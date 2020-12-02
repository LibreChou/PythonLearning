# Author:Zhang Yuan
from MyPackage import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import statsmodels.api as sm
from scipy import stats

#------------------------------------------------------------
__mypath__ = MyPath.MyClass_Path("")  # 路径类
mylogging = MyDefault.MyClass_Default_Logging(activate=False)  # 日志记录类，需要放在上面才行
myfile = MyFile.MyClass_File()  # 文件操作类
myword = MyFile.MyClass_Word()  # word生成类
myexcel = MyFile.MyClass_Excel()  # excel生成类
mytime = MyTime.MyClass_Time()  # 时间类
myplt = MyPlot.MyClass_Plot()  # 直接绘图类(单个图窗)
mypltpro = MyPlot.MyClass_PlotPro()  # Plot高级图系列
myfig = MyPlot.MyClass_Figure(AddFigure=False)  # 对象式绘图类(可多个图窗)
myfigpro = MyPlot.MyClass_FigurePro(AddFigure=False)  # Figure高级图系列
mynp = MyArray.MyClass_NumPy()  # 多维数组类(整合Numpy)
mypd = MyArray.MyClass_Pandas()  # 矩阵数组类(整合Pandas)
mypdpro = MyArray.MyClass_PandasPro()  # 高级矩阵数组类
myDA = MyDataAnalysis.MyClass_DataAnalysis()  # 数据分析类
myDefault = MyDefault.MyClass_Default_Matplotlib()  # 画图恢复默认设置类
# myMql = MyMql.MyClass_MqlBackups() # Mql备份类
# myBaidu = MyWebCrawler.MyClass_BaiduPan() # Baidu网盘交互类
# myImage = MyImage.MyClass_ImageProcess()  # 图片处理类
myBT = MyBackTest.MyClass_BackTestEvent()  # 事件驱动型回测类
myBTV = MyBackTest.MyClass_BackTestVector()  # 向量型回测类
myML = MyMachineLearning.MyClass_MachineLearning()  # 机器学习综合类
mySQL = MyDataBase.MyClass_MySQL(connect=False)  # MySQL类
mySQLAPP = MyDataBase.MyClass_SQL_APPIntegration()  # 数据库应用整合
myWebQD = MyWebCrawler.MyClass_QuotesDownload(tushare=False)  # 金融行情下载类
myWebR = MyWebCrawler.MyClass_Requests()  # Requests爬虫类
myWebS = MyWebCrawler.MyClass_Selenium(openChrome=False)  # Selenium模拟浏览器类
myWebAPP = MyWebCrawler.MyClass_Web_APPIntegration()  # 爬虫整合应用类
myEmail = MyWebCrawler.MyClass_Email()  # 邮箱交互类
myReportA = MyQuant.MyClass_ReportAnalysis()  # 研报分析类
myFactorD = MyQuant.MyClass_Factor_Detection()  # 因子检测类
myKeras = MyDeepLearning.MyClass_tfKeras()  # tfKeras综合类
myTensor = MyDeepLearning.MyClass_TensorFlow()  # Tensorflow综合类
myMT5 = MyMql.MyClass_ConnectMT5(connect=False)  # Python链接MetaTrader5客户端类
myMT5Pro = MyMql.MyClass_ConnectMT5Pro(connect=False)  # Python链接MT5高级类
myDefault.set_backend_default("Pycharm")  # Pycharm下需要plt.show()才显示图
#------------------------------------------------------------

'''
# 根据前面的范围过滤，我们筛选出了固定的指标和其固定的参数。那么，我们固定范围指标，调整策略参数，看看不同策略参数下，相同的范围过滤，会得出什么情况。
'''


#%%
########## 单次测试部分 #################
import warnings
warnings.filterwarnings('ignore')

# ---获取数据
symbol = "EURUSD"
timeframe = "TIMEFRAME_D1"

date_from, date_to = myMT5Pro.get_date_range(timeframe)
data_total = myMT5Pro.getsymboldata(symbol,timeframe,date_from,date_to,index_time=True, col_capitalize=True)
data_train, data_test = myMT5Pro.get_train_test(data_total, train_scale=0.8)

# 单独测试对全数据进行测试，训练集、测试集仅画区间就可以了
train_x0 = data_train.index[0]
train_x1 = data_train.index[-1]


#%%
# ---范围过滤的超空间稳定性
direct = "BuyOnly"
k_range = [k for k in range(50, 150+1)]
holding_range = [holding for holding in range(1, 1+1)]
lag_trade_range = [lag_trade for lag_trade in range(1, 1+1)]
# ---策略结果分析
out_list1 = []
out_list2 = []
# 选择夏普比和胜率来分析，下面的信号质量计算是否重复持仓都要分析。重复持仓主要看胜率。
label1 = "sharpe"
label2 = "winRate"
for k in k_range:
    for holding in holding_range:
        for lag_trade in lag_trade_range:
            # ---获取信号数据
            signaldata_buy = myBTV.stra.momentum(data_total.Close, k=k, holding=holding, sig_mode=direct, stra_mode="Continue")

            # ---(核心，在库中添加)获取指标
            indicator = myBTV.indi.get_oscillator_indicator(data_total, "roc", ("Close",92))

            # ---信号利润范围过滤及测试
            result = myBTV.rfilter.signal_range_filter_and_quality(signal_train=signaldata_buy[direct], signal_all=signaldata_buy[direct], indicator=indicator, price_DataFrame=data_total,price_Series=data_total.Close, holding=1, lag_trade=1, noRepeatHold=True, indi_name="roc", indi_para=("Close",92))

            out_list1.append(result[label1][0])
            out_list2.append(result[label2][0])
# ---
pd.Series(out_list1, index=k_range).plot()
plt.show()
myBTV.signal_quality_explain()






