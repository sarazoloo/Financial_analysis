import streamlit as st

import pandas as pd
import numpy as np

#Load Dataset
st.set_page_config(layout="wide")
st.title("Financial Analysis App")
st.write("Disclaimer: This is only for the analysis of general retail companies on the mongolian website mse.mn")

uploaded_file = st.file_uploader("Choose an excel file")

def get_balance_sheet(uploaded_file):
    dict_df = pd.read_excel(uploaded_file, sheet_name=[0,1])
    b_df = dict_df.get(0)
    return b_df

def get_income_sheet(uploaded_file):
    dict_df = pd.read_excel(uploaded_file, sheet_name=[0,1])
    i_df = dict_df.get(1)
    return i_df

    
#make an items dictionary for translation

items_dict = {'Мөнгө,түүнтэй адилтгах хөрөнгө': 'Cash and cash equivalents','Дансны авлага':'Accounts receivables',
              'Татвар, НДШ – ийн авлага':'Tax receivables','Бусад авлага':'Other receivables',
              'Бусад санхүүгийн хөрөнгө':'Other short-term asset', 'Бараа материал':'Inventory',
              'Урьдчилж төлсөн зардал/тооцоо':'Prepaid expense','Бусад эргэлтийн хөрөнгө':'Other current asset',
              'Борлуулах зорилгоор эзэмшиж буй эргэлтийн бус хөрөнгө (борлуулах бүлэг хөрөнгө)':'SDS', 
              'Эргэлтийн хөрөнгийн дүн':'Total current assets','Үндсэн хөрөнгө':'PPE','Биет бус хөрөнгө':'Intangible asset',
              'Биологийн хөрөнгө':'Biological asset','Урт хугацаат  хөрөнгө оруулалт':'Long-term investment',
              'Хойшлогдсон татварын хөрөнгө':'Deferred tax', 'Бусад эргэлтийн бус хөрөнгө':'Other non-current asset',
              'Эргэлтийн бус хөрөнгийн дүн':'Total non-current asset','Нийт хөрөнгийн дүн':'Total asset',
              'Дансны өглөг':'Accounts payable','Цалингийн  өглөг':'Salaries payable','Татварын өр':'Tax payable',
              'НДШ - ийн  өглөг':'Social securities payable','Богино хугацаат зээл':'Short-term debt',
              'Хүүний  өглөг':'Interest payable','Ногдол ашгийн  өглөг':'Dividend payable','Урьдчилж орсон орлого':'Unearned revenue',
              'Бусад богино хугацаат өр төлбөр':'Other short-term liabilities', 
              'Богино хугацаат өр төлбөрийн дүн':'Total current liabilities', 'Урт хугацаат зээл':'Long-term debt',
              'Хойшлогдсон татварын өр':'Deferred income tax', 'Бусад урт хугацаат өр төлбөр':'Other long-term liabilities',
              'Урт хугацаат өр төлбөрийн дүн':'Total long-term liabilities', 'Өр төлбөрийн нийт дүн':'Total liabilities',
              'Өмч':'Equity','    -хувийн':'Common stock', 'Хөрөнгийн дахин үнэлгээний нэмэгдэл':'Diluted stocks',
              'Хуримтлагдсан ашиг':'Retained earnings','Эздийн өмчийн дүн':'Stockholders equity',
              'Өр төлбөр ба эздийн өмчийн дүн':'Total liabilities and stockholders equity',
              'Борлуулалтын орлого (цэвэр)':'Revenue/sales', 'Борлуулалтын өртөг': 'COGS', 'Нийт ашиг ( алдагдал)': 'Gross profit',
              'Түрээсийн орлого':'Rent income', 'Хүүний орлого':'Interest income', 'Ногдол ашгийн орлого':'Dividend income', 
              'Бусад орлого':'Other income','Борлуулалт, маркетингийн зардал':'Sales, marketing expense', 
              'Ерөнхий ба удирдлагын зардал':'General, admin expense', 'Санхүүгийн зардал':'Finance expense', 
              'Бусад зардал':'Other expense', 'Гадаад валютын ханшийн зөрүүний  олз (гарз)':'Currency exchange gain/loss',
              'Үндсэн хөрөнгө данснаас хассаны олз (гарз)':'Sales of long term assets gain/ loss',
              'Биет бус хөрөнгө данснаас хассаны олз (гарз)':'Sales of non-current assets gain / loss',
              'Хөрөнгө оруулалт борлуулснаас үүссэн  олз (гарз)':'Investment gain/ loss', 
              'Татвар төлөхийн өмнөх  ашиг (алдагдал)':'EBT',
              'Орлогын татварын зардал':'Income tax', 'Тайлант үеийн цэвэр ашиг ( алдагдал)':'Net income'}

#Balance sheet data cleaning
def balance_df_clean(bs_df):
    bs_df = bs_df.drop(bs_df.iloc[:, :2], axis=1)
    bs_df = bs_df.dropna()
    bs_df = bs_df.reset_index(drop=True)
    bs_df = bs_df.rename(columns={"Unnamed: 2":"Items","Unnamed: 3":"Previous","Unnamed: 4":"Current"})
    bs_df = bs_df.drop(bs_df.index[:3]).reset_index(drop=True)
    bs_dict = pd.read_csv('balance_dict.csv')
    mask = bs_df['Items'].isin(bs_dict['Mongolian'])
    bs_df = bs_df.loc[mask].reset_index(drop=True)
    bs_df = bs_df.replace({"Items": items_dict})
    bs_df['Previous'] = bs_df['Previous'].astype(int)
    bs_df['Current'] = bs_df['Current'].astype(int)
    
    bs_df.to_csv('balance_sheet.csv', index=False)
    return bs_df


#Income statement data cleaning
def income_df_clean(is_df):
    is_df = is_df.drop(is_df.iloc[:, :2], axis=1)
    is_df = is_df.dropna()
    is_df = is_df.reset_index(drop=True)
    is_df = is_df.rename(columns={"Unnamed: 2":"Items","Unnamed: 3":"Previous","Unnamed: 4":"Current"})
    is_df = is_df.drop(is_df.index[:1]).reset_index(drop=True)
    is_dict = pd.read_csv("income_dict.csv")
    mask1 = is_df['Items'].isin(is_dict['Mongolian'])
    is_df = is_df.loc[mask1].reset_index(drop=True)
    is_df = is_df.replace({"Items": items_dict})
    is_df['Previous'] = is_df['Previous'].astype(int)
    is_df['Current'] = is_df['Current'].astype(int)
    
    is_df.to_csv('income_sheet.csv', index=False)
    return is_df


if uploaded_file is not None:
    
    bs_raw = get_balance_sheet(uploaded_file)
    balance_sheet = balance_df_clean(bs_raw)
    #st.write("balance_sheet", balance_sheet)
    
    is_raw = get_income_sheet(uploaded_file)
    income_sheet = income_df_clean(is_raw)
    #st.write("income_sheet", income_sheet)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Balance Sheet")
        st.write(balance_sheet)
        
    with col2:
        st.header("Income Statement")
        st.write(income_sheet)
    


st.subheader("Ratio Analysis")
n = '\n'
description1 = (f""" 
This is a simple ratio analysis including: {n}
Liquidity ratios: Current ratio, Quick ratio, Cash ratio {n}
Long-term solvency ratios: Total debt, Debt-to-equity, Equity multiplier {n}
Asset utilization ratios: Receivables turnover, Days in sales receivables, Inventory turnover, Days in sales inventory, Accounts payable turnover, Total asset turnover {n}
Profitability ratios: Profit margin, ROE, ROA, DU-PONT """)

st.write(description1)


#Industry Benchmark 
dict_benchmark = pd.read_excel("benchmark.xlsx", sheet_name=['Benchmark'])
benchmark_df = dict_benchmark.get('Benchmark')

st.write('Industry Average Benchmark', benchmark_df)



# Ratio calculation functions
def current_ratio(quarter):
    ca = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total current assets'].index, balance_sheet.columns.get_loc(quarter)].values
    cl = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total current liabilities'].index, balance_sheet.columns.get_loc(quarter)].values
    current = ca / cl
    return current

def quick_ratio(quarter):
    cash = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Cash and cash equivalents'].index, balance_sheet.columns.get_loc(quarter)].values
    sds = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'SDS'].index, balance_sheet.columns.get_loc(quarter)].values
    ar = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Accounts receivables'].index, balance_sheet.columns.get_loc(quarter)].values
    tr = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Tax receivables'].index, balance_sheet.columns.get_loc(quarter)].values
    other_r = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Other receivables'].index, balance_sheet.columns.get_loc(quarter)].values
    
    cl = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total current liabilities'].index, balance_sheet.columns.get_loc(quarter)].values
    
    quick = (cash + sds + ar + tr + other_r) / cl
    return quick

def cash_ratio(quarter):
    cash = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Cash and cash equivalents'].index, balance_sheet.columns.get_loc(quarter)].values
    sds = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'SDS'].index, balance_sheet.columns.get_loc(quarter)].values
    cl = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total current liabilities'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = (cash + sds) / cl
    return result

def td_ratio(quarter):
    short_debt = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Short-term debt'].index, balance_sheet.columns.get_loc(quarter)].values
    long_debt = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Long-term debt'].index, balance_sheet.columns.get_loc(quarter)].values
    
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = (short_debt + long_debt) / ta
    return result

def debt_equity_ratio(quarter):
    short_debt = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Short-term debt'].index, balance_sheet.columns.get_loc(quarter)].values
    long_debt = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Long-term debt'].index, balance_sheet.columns.get_loc(quarter)].values
    
    te = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = (short_debt + long_debt) / te
    return result

def equity_multiplier_ratio(quarter):
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc(quarter)].values
    te = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = ta / te
    return result

def receivables_turnover_ratio(quarter):
    sales = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Revenue/sales'].index, income_sheet.columns.get_loc(quarter)].values
    ar = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Accounts receivables'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = sales / ar
    return result

def inventory_turnover_ratio(quarter):
    cogs = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'COGS'].index, income_sheet.columns.get_loc(quarter)].values
    inv = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Inventory'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = cogs / inv
    return result

def accounts_payable_ratio(quarter):
    cogs = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'COGS'].index, income_sheet.columns.get_loc(quarter)].values
    ap = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Accounts payable'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = cogs / ap
    return result

def ta_turnover_ratio(quarter):
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc(quarter)].values
    sales = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Revenue/sales'].index, income_sheet.columns.get_loc(quarter)].values
    
    result = sales / ta
    return result

def profit_margin_ratio(quarter):
    ni = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Net income'].index, income_sheet.columns.get_loc(quarter)].values
    sales = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Revenue/sales'].index, income_sheet.columns.get_loc(quarter)].values
    
    result = ni / sales
    return result

def roe_ratio(quarter):
    ni = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Net income'].index, income_sheet.columns.get_loc(quarter)].values
    te = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = ni / te
    return result

def roa_ratio(quarter):
    ni = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Net income'].index, income_sheet.columns.get_loc(quarter)].values
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc(quarter)].values
    
    result = ni / ta
    return result

#Ratio calculation for the previous year


def load_ratio():
    return pd.DataFrame(
        {
            "Ratio ": ["Current", "Quick", "Cash", "Total Debt", "Debt-to-Equity","Equity multiplier",
                      "Receivables Turnover", "Days in sales in receivables", "Inventory Turnover", "Days in sales in inventory",
                      "Accounts payable", "Total asset turnover", "Profit margin", "ROE", "ROA", "DU-PONT"],
            "Previous": [current_ratio("Previous"), quick_ratio("Previous"), cash_ratio("Previous"),td_ratio("Previous"),
                        debt_equity_ratio("Previous"), equity_multiplier_ratio("Previous"), receivables_turnover_ratio("Previous"),
                        (365 / receivables_turnover_ratio("Previous")),inventory_turnover_ratio("Previous"),
                        (365 / inventory_turnover_ratio("Previous")), accounts_payable_ratio("Previous"), 
                        ta_turnover_ratio("Previous"), profit_margin_ratio("Previous"), roe_ratio("Previous"),
                        roa_ratio("Previous"), 
                        (profit_margin_ratio("Previous") + ta_turnover_ratio("Previous") + equity_multiplier_ratio("Previous")) ],
            "Current": [current_ratio("Current"), quick_ratio("Current"), cash_ratio("Current"),td_ratio("Current"),
                        debt_equity_ratio("Current"), equity_multiplier_ratio("Current"), receivables_turnover_ratio("Current"),
                        (365 / receivables_turnover_ratio("Current")),inventory_turnover_ratio("Current"),
                        (365 / inventory_turnover_ratio("Current")), accounts_payable_ratio("Current"), 
                        ta_turnover_ratio("Current"), profit_margin_ratio("Current"), roe_ratio("Current"),
                        roa_ratio("Current"), 
                        (profit_margin_ratio("Current") + ta_turnover_ratio("Current") + equity_multiplier_ratio("Current")) ]
        }
    )

def convert_df(df):
    return df.to_csv().encode('utf-8')

run_button = st.button("Run ratio analysis")
if run_button:
    df = load_ratio()
    csv = convert_df(df)
    st.write("Analysis completed", df)
    st.download_button(label="Download data as CSV", data=csv, file_name='ratio_df.csv', mime='text/csv')
    
    
# Prospective forecast analysis

st.subheader("Prospective forecast analysis")
description2 = (f'''
This forecast uses a simple prospective analysis to use. The percentages are averaged and used to calculate the upcoming year. The forecast takes the average of the two years of total asset, total liabilities, and stockholders equity as 100% and multiplies the sub-items.''')
st.write(description2)

#forecast calulcations

#previous year forecast precentage calculations
def prev_balance_forecast():
    ta_index = balance_sheet[balance_sheet['Items']=='Total asset'].index.values
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index,balance_sheet.columns.get_loc("Previous")].values
    
    cl_index = balance_sheet[balance_sheet['Items']=='Total liabilities'].index.values
    tl = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index,balance_sheet.columns.get_loc("Previous")].values
    
    se_index = balance_sheet[balance_sheet['Items']=='Stockholders equity'].index.values
    se = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index,balance_sheet.columns.get_loc("Previous")].values
    
    for a in range(0, (2 +int(ta_index))):
        ta_perc =  ((balance_sheet["Previous"][:a] / ta)*100).round(2)
    
    for b in range((int(ta_index)), (2 + int(cl_index))):
        bs = (1 + int(ta_index))
        tl_perc = ((balance_sheet["Previous"][bs:b] / tl)*100).round(2)
    
    for c in range((int(cl_index)), (2 + int(se_index))):
        ci = (1 + int(cl_index))
        se_perc = ((balance_sheet["Previous"][ci:c] / se)*100).round(2) 
        
    prev = pd.concat([ta_perc, tl_perc, se_perc])
    balance_sheet["Previous %"] = prev.tolist()
    
    return balance_sheet

#current year percentage calculations
def current_balance_forecast():
    ta_index = balance_sheet[balance_sheet['Items']=='Total asset'].index.values
    ta = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc("Current")].values
    
    tl_index = balance_sheet[balance_sheet['Items']=='Total liabilities'].index.values
    tl = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index, balance_sheet.columns.get_loc("Current")].values
    
    se_index = balance_sheet[balance_sheet['Items']=='Stockholders equity'].index.values
    se = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc("Current")].values
    
    for a in range(0, (2 +int(ta_index))):
        ta_perc =  ((balance_sheet["Current"][:a] / ta)*100).round(2)
    
    for b in range((int(ta_index)), (2 + int(tl_index))):
        bs = (1 + int(ta_index))
        tl_perc = ((balance_sheet["Current"][bs:b] / tl)*100).round(2)
    
    for c in range((int(tl_index)), (2 + int(se_index))):
        ci = (1 + int(tl_index))
        se_perc = ((balance_sheet["Current"][ci:c] / se)*100).round(2)
        
    prev = pd.concat([ta_perc, tl_perc, se_perc])
    balance_sheet["Current %"] = prev.tolist()
    
    return balance_sheet

#averaging the two percentages
def ave_forecast():
    balance_sheet['Average %'] = (balance_sheet["Previous %"] +  balance_sheet["Current %"]) / 2
    
    return balance_sheet

#actual forecast calculations of upcoming year with the average percentages
def balance_forecast_year1():
    ta_index = balance_sheet[balance_sheet['Items']=='Total asset'].index.values    
    tl_index = balance_sheet[balance_sheet['Items']=='Total liabilities'].index.values    
    se_index = balance_sheet[balance_sheet['Items']=='Stockholders equity'].index.values
    
    ta_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc("Previous")].values
    ta_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc("Current")].values
    
    tl_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index, balance_sheet.columns.get_loc("Previous")].values
    tl_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index, balance_sheet.columns.get_loc("Current")].values

    se_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc("Previous")].values
    se_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc("Current")].values
    
    ta_year1 = (ta_prev + ta_cur)/2
    ta_to_tl = ((ta_prev / tl_prev) + (ta_cur / tl_cur)) / 2
    tl_year1 = ta_year1 * ta_to_tl
    ta_to_se = ((ta_prev / se_prev) + (ta_cur / se_cur)) / 2
    
    se_year1 = ta_year1 * ta_to_se
    
    for a in range(0, 1 + (int(ta_index))):
        ta_forecast =  (ta_year1 * ((balance_sheet["Average %"][:a] / 100))).astype(np.int64, errors='ignore')
    
    for b in range(int(ta_index), 1+ (int(tl_index))):
        bs = (1 + int(ta_index))
        tl_forecast = (tl_year1 * ((balance_sheet["Average %"][bs:b]) / 100)).astype(np.int64, errors='ignore')
    
    for c in range((int(tl_index)), 1 + (int(se_index))):
        ci = (1 + int(tl_index))
        se_forecast = (se_year1 * ((balance_sheet["Average %"][ci:c]) / 100 )).astype(np.int64, errors='ignore')
        
    
    forecast1 = pd.concat([ta_forecast, tl_forecast, se_forecast])
    balance_sheet["Forecast"] = forecast1
    
    return balance_sheet

#fill in the nans of total asset, total liabilities, and stockholders equity
def fill_nan1():
    ta_index = balance_sheet[balance_sheet['Items']=='Total asset'].index.values    
    tl_index = balance_sheet[balance_sheet['Items']=='Total liabilities'].index.values    
    se_index = balance_sheet[balance_sheet['Items']=='Stockholders equity'].index.values
    
    ta_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc("Previous")].values
    ta_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total asset'].index, balance_sheet.columns.get_loc("Current")].values
    
    tl_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index, balance_sheet.columns.get_loc("Previous")].values
    tl_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Total liabilities'].index, balance_sheet.columns.get_loc("Current")].values

    se_prev = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc("Previous")].values
    se_cur = balance_sheet.iloc[balance_sheet[balance_sheet['Items'] == 'Stockholders equity'].index, balance_sheet.columns.get_loc("Current")].values
    
    ta_forecast1 = ((ta_prev + ta_cur) / 2).astype(np.int64)
    balance_sheet.iloc[ta_index, balance_sheet.columns.get_loc("Forecast")] = ta_forecast1
    
    ta_to_tl = ((ta_prev / tl_prev) + (ta_cur / tl_cur)) / 2
    tl_forecast1 = (ta_forecast1 * ta_to_tl).astype(np.int64)
    balance_sheet.iloc[tl_index, balance_sheet.columns.get_loc("Forecast")] = tl_forecast1
    
    ta_to_se = ((ta_prev / se_prev) + (ta_cur / se_cur)) / 2
    se_forecast1 = (ta_forecast1 * ta_to_se).astype(np.int64)
    balance_sheet.iloc[se_index, balance_sheet.columns.get_loc("Forecast")] = se_forecast1
    
    return balance_sheet

run_button2 = st.button("Run Balance Sheet prospective analysis")
if run_button2:
    df1 = prev_balance_forecast()
    df1 = current_balance_forecast()
    df1 = ave_forecast()
    df1 = balance_forecast_year1()
    df1 = fill_nan1()
    csv = convert_df(df1)
    st.write("Balance Sheet analysis completed", df1)
    st.download_button(label="Download data as CSV", data=csv, file_name='bs_df.csv', mime='text/csv')
    
    
def income_forecast():
    rev_index = income_sheet[income_sheet['Items']=='Revenue/sales'].index.values
    rev_p = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Revenue/sales'].index, income_sheet.columns.get_loc("Previous")].values
    rev_c = income_sheet.iloc[income_sheet[income_sheet['Items'] == 'Revenue/sales'].index, income_sheet.columns.get_loc("Current")].values

    i = len(income_sheet)
    rev_prev =  ((income_sheet["Previous"][:i] / rev_p)*100).round(2)
    rev_curr = ((income_sheet["Current"][:i] / rev_c)*100).round(2)
    
    income_sheet["Previous %"] = rev_prev
    income_sheet["Current %"] = rev_curr
    income_sheet['Average %'] = (rev_prev + rev_curr) / 2

    ave_rev = (rev_p + rev_c) / 2
    rev_forecast = (ave_rev * (income_sheet["Average %"][:i] / 100)).astype(np.int64, errors='ignore')

    income_sheet["Forecast"] = rev_forecast
    
    return income_sheet

run_button3 = st.button("Run prospective analysis for Income Statement")
if run_button3:
    df2 = income_forecast()
    csv = convert_df(df2)
    st.write("Income Statement analysis completed", df2)
    st.download_button(label="Download data as CSV", data=csv, file_name='is_df.csv', mime='text/csv')

#if __name__ == '__main__':
#    main()
