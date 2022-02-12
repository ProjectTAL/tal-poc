from tkinter.ttk import Combobox
import sys
from strategy.RSIStrategy import *
from tkinter import *
from util.time_helper import *

app = QApplication(sys.argv)

# 필요할 때마다 kiwoom API 가져다 쓰기 위해 instance 생성
mKiwoomInstance = Kiwoom()

# 계좌를 가져오며, 1개 이상의 계좌번호를 가져올 경우, Combobox에 하나씩 넣기 위해 구성
mAccountNumbers = mKiwoomInstance.get_account_number()
mAccountNumbers = mAccountNumbers.split(';')
mAccountTotalNum = 0
for i in mAccountNumbers[:-1]:
    mAccountTotalNum += 1

mDeposit = mKiwoomInstance.get_deposit_tal(mAccountNumbers[0])  # 예수금 가져오기







# Tkinter GUI 사용
window = Tk()
window.title("Thanks A Lot")
window.geometry("1050x600")
window.resizable(0, 0)

# 1st 요구사항 : 자산현황 확인. (잔고, 예수금 출력)
balanceLFrame = LabelFrame(window, text="자산현황", padx=10, pady=10)
balanceLFrame.pack()
balanceLFrame.place(x=20, y=20)

accountCBox = Combobox(balanceLFrame, width=12, state='readonly')
accountCBox['values'] = [mAccountNumbers[m] for m in range(0, mAccountTotalNum)]
accountCBox.current(0)
accountCBox.grid(row=0, column=0)

def getBalance():
    balanceLBox.delete(0, END)
    # 잔고 가져오기
    balance = mKiwoomInstance.get_balance_tal(accountCBox.get())
    print(balance)
    for key, value in balance.items():
        for key1, value1 in value.items():
            balanceLBox.insert(END, str(key1) + " : " + str(value1))
        balanceLBox.insert(END, "......")
    accountCBox.config(state='disabled')

# 잔고 : 현재 보유 중인 종목들.
getBalanceButton = Button(balanceLFrame, text="잔고 불러오기", command=getBalance)
getBalanceButton.grid(row=0, column=1)

mDepositVar = StringVar()
mDepositVar.set("{:,}".format(mDeposit) + "원")

depositTitleLabel = Label(balanceLFrame, text="보유현금(예수금):")
depositTitleLabel.grid(row=1, column=0)
depositContentsLabel = Label(balanceLFrame, textvariable=mDepositVar, width=15)
depositContentsLabel.grid(row=1, column=1)

balanceLBox = Listbox(balanceLFrame)
balanceLBox.grid(row=2, column=0)

mMarketOpenVar = StringVar()
if not check_transaction_open():
    mMarketOpenVar.set("※ 장시간이 아닙니다 (09:00~15:20)")
else:
    mMarketOpenVar.set("☆★ 장시간 입니다~!")

marketOpenLabel = Label(window, textvariable=mMarketOpenVar)
marketOpenLabel.place(x=20, y=270)

if not check_transaction_open():
    marketOpenLabel.config(fg="red")
else:
    marketOpenLabel.config(fg="green")

def changeAccount(event):
    global mDeposit
    mDeposit = mKiwoomInstance.get_deposit_tal(accountCBox.get())
    mDepositVar.set("{:,}".format(mDeposit) + "원")
    if not check_transaction_open():
        mMarketOpenVar.set("※ 장시간이 아닙니다 (09:00~15:20)")
        marketOpenLabel.config(fg="red")
    else:
        mMarketOpenVar.set("☆★ 장시간 입니다~!")
        marketOpenLabel.config(fg="green")

# Todo : Refactoring from here
accountCBox.bind('<<ComboboxSelected>>', changeAccount)

labelFrame_2 = LabelFrame(window, text="매수하기", padx=10, pady=10)
labelFrame_2.pack()
labelFrame_2.place(x=305, y=20)

codeEdit = Entry(labelFrame_2, width=20)
codeEdit.insert(0, 'Enter code')
codeEdit.grid(row=0, column=0)


def click(event):
    codeEdit.configure(state=NORMAL)
    codeEdit.delete(0, END)
    codeEdit.unbind('<Button-1>', clicked)


clicked = codeEdit.bind('<Button-1>', click)

stockName = StringVar()
stockName.set("empty")

currentPrice = StringVar()
currentPrice.set("- 원")

kospi_code_list = mKiwoomInstance.get_code_list_by_market("0")
kosdak_code_list = mKiwoomInstance.get_code_list_by_market("10")


def SearchName():
    flag = False
    if codeEdit.get() in kospi_code_list:
        print("ok_kospi")
        flag = True
    elif codeEdit.get() in kosdak_code_list:
        print("ok_kosdak")
        flag = True
    if flag:
        code_name = mKiwoomInstance.get_master_code_name(codeEdit.get())
        stockName.set(code_name)
        current_price = mKiwoomInstance.get_now_price_tal(codeEdit.get())
        currentPrice.set("{:,}원".format(current_price))
        print(f"종목명 : {code_name}, 현재가 : {current_price}")
    else:
        stockName.set("정상코드아님")
        currentPrice.set("--")
        print("It is not correct code!!")


buttonNext = Button(labelFrame_2, text="Search", command=SearchName)
buttonNext.grid(row=0, column=1)

codeLabel = Label(labelFrame_2, textvariable=stockName)
codeLabel.grid(row=1, column=0)
currentPriceLabel = Label(labelFrame_2, width=10, textvariable=currentPrice)
currentPriceLabel.grid(row=1, column=1)

emptyLine = Label(labelFrame_2, text="")
emptyLine.grid(row=2, column=0)

# On:시장가, Off:지정가
isOn = True
on = PhotoImage(file="on.png").subsample(2)
off = PhotoImage(file="off.png").subsample(2)

buyWayText = StringVar()
buyWayText.set("<<시장가>>")


def switch():
    global isOn
    if isOn:
        on_button.config(image=off)
        buyWayText.set("<<지정가>>")
        priceSelectLabel.config(fg="blue")
        priceLabel.config(state='normal')
        priceEdit.config(state='normal')
        isOn = False
    else:
        on_button.config(image=on)
        buyWayText.set("<<시장가>>")
        priceSelectLabel.config(fg="green")
        priceLabel.config(state='disabled')
        priceEdit.config(state='disabled')
        isOn = True


on_button = Button(labelFrame_2, image=on, bd=0, command=switch)
on_button.grid(row=3, column=0)
priceSelectLabel = Label(labelFrame_2, textvariable=buyWayText, fg="green")
priceSelectLabel.grid(row=3, column=1)

countLabel = Label(labelFrame_2, text="구매 수량(개):")
countLabel.grid(row=4, column=0)
countEdit = Entry(labelFrame_2, width=10)
countEdit.grid(row=4, column=1)

priceLabel = Label(labelFrame_2, text="구매 금액(원):")
priceLabel.config(state='disabled')
priceLabel.grid(row=5, column=0)
priceEdit = Entry(labelFrame_2, width=10)
priceEdit.config(state='disabled')
priceEdit.grid(row=5, column=1)

buyResultText = StringVar()
buyResultText.set("...")

refreshValue = 0
refreshText = ""


def try2BUY():
    global refreshValue, refreshText
    refreshValue += 1
    if refreshValue > 5:
        refreshValue = 0
        refreshText = ""
    # listBoxBuy.delete(0, END)
    refreshText = refreshText + "*"
    helpText = ""
    flag = False
    if codeEdit.get() in kospi_code_list:
        print("ok_kospi")
        flag = True
    elif codeEdit.get() in kosdak_code_list:
        print("ok_kosdak")
        flag = True
    if not flag:
        helpText = refreshText + "code가 validate하지 않아요"
        buyResultText.set(helpText)
        listBoxBuy.insert(0, helpText)
        buyResultLabel.config(fg="red")
        return
    global isOn
    if isOn:  # 시장가
        code = codeEdit.get()
        count = countEdit.get()
        helpText = refreshText + "{}종목/시장가/{}개 시도".format(code, count)
        buyResultText.set(helpText)
        listBoxBuy.insert(0, helpText)
        buyResultLabel.config(fg="green")
        orderResult = mKiwoomInstance.send_order_tal('send_buy_order', '1002', 1, code, count, 0, '03',
                                                     accountCBox.get())
        print(f"시장가 주문 결과 : ", orderResult)
    else:  # 지정가
        code = codeEdit.get()
        count = countEdit.get()
        price = priceEdit.get()
        helpText = refreshText + "{}종목/지정가/{}원/{}개 시도".format(code, price, countEdit.get())
        buyResultText.set(helpText)
        listBoxBuy.insert(0, helpText)
        buyResultLabel.config(fg="blue")
        orderResult = mKiwoomInstance.send_order_tal('send_buy_order', '1002', 1, code, count, price, '00',
                                                     accountCBox.get())
        print(f"시장가 주문 결과 : ", orderResult)


buyResultLabel = Label(labelFrame_2, textvariable=buyResultText, width=40)
buyResultLabel.grid(row=6, column=0)

buyButton = Button(labelFrame_2, text="구매시도", command=try2BUY)
buyButton.grid(row=6, column=1)

listBoxBuy = Listbox(labelFrame_2, width=40, height=5)
listBoxBuy.grid(row=7)

labelFrame_3 = LabelFrame(window, text="매도하기", padx=10, pady=10)
labelFrame_3.pack()
labelFrame_3.place(x=700, y=20)

codeDictionary4CheckBox = {}
codeNameList = []
codeAmountList = []
boxes = []
entryBoxes = []
entryCountBoxes = []
sellDictionary = {}

# OnSell:시장가, OffSell:지정가
isOnSell = True
onSell = PhotoImage(file="on.png").subsample(2)
offSell = PhotoImage(file="off.png").subsample(2)


def checkedCode():
    print("checked()")
    global sellDictionary
    sellDictionary = {}
    for index, value in enumerate(boxes):
        if value[1].get() == 1:
            print(f"{codeNameList[index]} / {codeAmountList[index]}")
            sellDictionary[codeNameList[index]] = codeAmountList[index]
    print("-----------------------")
    print(sellDictionary)


def getMyList():
    print("get my list")
    # Initialize
    global boxes, codeNameList, codeAmountList, codeDictionary4CheckBox, isOnSell, entryBoxes, entryCountBoxes
    for index, value in enumerate(boxes):
        value[2].destroy()
    boxes = []
    codeNameList = []
    codeAmountList = []
    codeDictionary4CheckBox = {}
    entryBoxes = []
    entryCountBoxes = []

    position = mKiwoomInstance.get_balance_tal(accountCBox.get())
    for key, value in position.items():
        for key1, value1 in value.items():
            if "종목명" in key1:
                print(f"{key1} : {value1}")
                codeNameList.append(value1)
                codeDictionary4CheckBox[value1] = key
            if "보유수량" in key1:
                print(f"{key1} : {value1}")
                codeAmountList.append(value1)

    for i, j in enumerate(codeNameList):  # what ever loop you want
        varPrice = IntVar()
        bPrice = Entry(labelFrame_3, width=10, textvariable=varPrice)
        bPrice.grid(row=i + 3, column=2)
        if isOnSell:
            bPrice.config(state='disabled')
        else:
            bPrice.config(state='normal')
        entryBoxes.append([varPrice, bPrice])
        print(f"entry - {varPrice} / {bPrice}")
        varCount = IntVar()
        b = Entry(labelFrame_3, width=10, textvariable=varCount)
        b.insert(0, codeAmountList[i])
        b.grid(row=i + 3, column=1)
        b.delete(1)
        entryCountBoxes.append([varCount, b])
        var = IntVar()
        c = Checkbutton(labelFrame_3, text=j, variable=var, command=checkedCode)
        c.grid(row=i + 3, column=0, sticky="w")
        boxes.append([j.strip(), var, c])
        print(f"checkbox - {j.strip()} / {var} / {c} / {i} / {codeAmountList[i]}")


def sellStock():
    print("\nsellStock()")
    for index, value in enumerate(boxes):
        if value[1].get() == 1:
            code = codeDictionary4CheckBox[value[0]]
            quantity = entryCountBoxes[index][1].get()
            ask = entryBoxes[index][1].get()
            print(f"종목명:{value[0]} "
                  f"/ 수량:{quantity} "
                  f"/ 금액:{ask} "
                  f"/ 종목코드:{code}")
            if isOnSell:  # 시장가
                order_result = mKiwoomInstance.send_order_tal('send_sell_order', '1002', 2, code, quantity, 0, '03',
                                                              accountCBox.get())
                print(f"sellStock(시장가) - {order_result}")
            else:  # 지정가
                order_result = mKiwoomInstance.send_order_tal('send_sell_order', '1002', 2, code, quantity, ask, '00',
                                                              accountCBox.get())
                print(f"sellStock(지정가) - {order_result}")


getListButton = Button(labelFrame_3, text="내주식 불러오기", command=getMyList, width=20)
getListButton.grid(row=0, column=0)

sellStockButton = Button(labelFrame_3, text="주식 팔기", command=sellStock, width=10)
sellStockButton.grid(row=0, column=1)

sellWayText = StringVar()
sellWayText.set("<<시장가>>")


def switchSell():
    global isOnSell
    if isOnSell:
        on_button_sell.config(image=offSell)
        sellWayText.set("<<지정가>>")
        sellPriceSelectLabel.config(fg="blue")
        # priceLabel.config(state='normal')
        # priceEdit.config(state='normal')
        for index, value in enumerate(entryBoxes):
            value[1].config(state='normal')
        isOnSell = False
    else:
        on_button_sell.config(image=onSell)
        sellWayText.set("<<시장가>>")
        sellPriceSelectLabel.config(fg="green")
        for index, value in enumerate(entryBoxes):
            value[1].config(state='disabled')
        isOnSell = True


on_button_sell = Button(labelFrame_3, image=onSell, bd=0, command=switchSell)
on_button_sell.grid(row=1, column=0)
sellPriceSelectLabel = Label(labelFrame_3, textvariable=sellWayText, fg="green")
sellPriceSelectLabel.grid(row=1, column=2)

sellLabel1 = Label(labelFrame_3, text="종목명")
sellLabel1.grid(row=2, column=0)

sellLabel2 = Label(labelFrame_3, text="수량(개)")
sellLabel2.grid(row=2, column=1)

sellLabel2 = Label(labelFrame_3, text="금액(원)")
sellLabel2.grid(row=2, column=2)

labelFrame_4 = LabelFrame(window, text="주문 예약 현황", padx=10, pady=10)
labelFrame_4.pack()
labelFrame_4.place(x=20, y=330)


def callReserv():
    print("\nreserv")
    orders = mKiwoomInstance.get_order_tal(accountCBox.get())
    empty = ""
    print(orders)
    listBoxResev.insert(0, empty)
    listBoxResev.insert(0, orders)


on_button_reserv_call = Button(labelFrame_4, text="불러오기", command=callReserv)
on_button_reserv_call.grid(row=1, column=0)
emptyLine_4 = Label(labelFrame_4, text="")
emptyLine_4.grid(row=2, column=0)
listBoxResev = Listbox(labelFrame_4, width=80, height=10)
listBoxResev.grid(row=3)

codeEdit.focus_force()
window.mainloop()
app.exec()
