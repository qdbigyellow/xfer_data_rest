from financial_modeling.company_data_to_tsdb import gauge_dict

class TestCompanyDataToDSTB:
    def test_pass(self):
        assert True

    def test_gauge_dict_return_defaultvalue(self):
        d = gauge_dict()
        assert "see gauge name" == d["anything"] 
        assert "Gross Profit Groth" == d["gross_profit_growth"]
        assert "Share price to Book value. Less than one means share is under valued" == d['pb_ratio']




