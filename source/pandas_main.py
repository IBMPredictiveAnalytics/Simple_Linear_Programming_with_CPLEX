# encoding=utf-8
'''
Created on Jan 9, 2017

@author: weyu
'''

from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
import sys,pandas,json
from docplex.mp.model import Model
from collections import namedtuple
from pyspark.sql.types import StructField, StructType, StringType, DoubleType, IntegerType

ascontext=None
if len(sys.argv) > 1 and sys.argv[1] == "-test":
    sc = SparkContext('local')
    sqlContext = SQLContext(sc)
    data = sqlContext.createDataFrame(pandas.read_csv("C:\\Users\\weyu\\Documents\\awork_spss\\cplex\\wheat_or_barley_en.csv"))
    limitationInput = "wheat_or_barley_limitation.py"
    input_name = "name"
    input_qmin = "qmin"
    input_qmax = "qmax"
    input_optimise = "Price"
else:
    import spss.pyspark.runtime
    ascontext = spss.pyspark.runtime.getContext()
    sc = ascontext.getSparkContext()
    sqlContext = ascontext.getSparkSQLContext()
    data = ascontext.getSparkInputData()
    limitationInput = "%%input_file_nutrients%%"
    input_name = "%%input_col_name%%"
    input_qmin = "%%input_col_qmin%%"
    input_qmax = "%%input_col_qmax%%"
    input_optimise = "%%input_col_cost%%"

execfile(limitationInput)

Limitation = namedtuple("Limitation", ["name", "qmin", "qmax"])
limitation = [Limitation(*row) for row in LIMITATION]

outputSchema = StructType([StructField("index", IntegerType(), False),
                          StructField("name", StringType(), False),
                          StructField("value", DoubleType(), False)])

if ascontext != None and ascontext.isComputeDataModelOnly():
    ascontext.setSparkOutputSchema(outputSchema)
else:
    data = data.toPandas()
    mdl = Model(name='simple_linear_programming')
    qty = {f[2]: mdl.continuous_var(lb=f[0], ub=f[1], name=f[2]) 
        for f in [tuple(x) for x in data[[input_qmin, input_qmax, input_name]].values.tolist()]}
            
    data = data.set_index(input_name,drop=False)
    itemlist = data.index
        
    for n in limitation:
        limitationdata = data[n.name].to_dict()
        amount = mdl.sum(qty[f] * limitationdata[f] for f in itemlist)
        mdl.add_range(n.qmin, amount, n.qmax)
        mdl.add_kpi(amount, publish_name="Total %s" % n.name)
            
    optimisedata = data[input_optimise].to_dict()
    mdl.maximize(mdl.sum(qty[f] * optimisedata[f] for f in itemlist))
    mdl.solve()
    mdl.print_information()
    mdl.print_solution()
    data = json.loads(mdl.solution.export_as_string())
    coredata = data['CPLEXSolution']['variables']
    pandas_df = pandas.read_json(json.dumps(coredata))
    spark_df = sqlContext.createDataFrame(pandas_df)
    if ascontext != None:
        ascontext.setSparkOutputData(spark_df)
    else:
        spark_df.show()

