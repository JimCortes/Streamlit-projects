companies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
companies = companies[0]
symbols = companies["Symbol"].tolist()
indicators = {
    "Market Cap": "marketCap",
    "Book Value": "bookValue",
    "Fiscal year":"lastFiscalYearEnd",
    "Regular Market Price" : "regularMarketPrice",
    "Enterprice Value":"enterpriseValue",
    }


title = """
<div style="font-size:60px;font-weight:bolder;background-color:#fff;text-align:center;">
		<span style='color:Green'>SP 500</span>
		
</div>

"""
dics = {

    "Deep": Focus ,
}


stc.html(title)
st.sidebar.subheader("Menu")
