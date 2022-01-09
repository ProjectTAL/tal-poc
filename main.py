from api.Kiwoom import *
import sys

app = QApplication(sys.argv)
kiwoom = Kiwoom()
# kiwoom.get_account_number()

deposit = kiwoom.get_deposit()

# ToDO : 여기서 007700 종목을 정상적으로 1)주문 접수, 2)주문 체결, 3)잔고 이동 하는지 확인 할 것.
# 사용자 구분, 화면 번호, 주문 유형 (1:신규 매수, 2:신규 매도, ...), 종목코드, 주문수량, 주문가격, 거래구분(00:지정가, 03:시장가,...)
order_result = kiwoom.send_order('send_by_order', '1001', 1, '007700', 1, 30000, '00')

# df = kiwoom.get_price_data("005930")
# print(df)
# kospi_code_list = kiwoom.get_code_list_by_market("0")
# for code in kospi_code_list:
#     code_name = kiwoom.get_master_code_name(code)
#     print(code, code_name)
#
# kosdaq_code_list = kiwoom.get_code_list_by_market("10")
# for code in kosdaq_code_list:
#     code_name = kiwoom.get_master_code_name(code)
#     print(code, code_name)

app.exec_()
