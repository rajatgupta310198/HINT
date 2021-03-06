import datetime
import random
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from . import get_online_data
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class Neon_Engine:

    def __init__(self):
        self.clf = KNeighborsClassifier()

    def getdata_and_train(self,train_no):
        get_online_data.Create_DataFile(train_no)
        df = pd.read_csv('.data.csv')
        df.fillna(value=0, inplace=True)
        new_df = df.apply(LabelEncoder().fit_transform)
        X = new_df.drop(['Status'], axis=1)
        X = X.drop(['Reach Time'], axis=1)
        y = new_df['Status']
        self.clf.fit(X, y)

        # Train the model of particular locomotive
        # Example : Get train data from user. convert results to DataFrame and feed it.

    def predict_delay(self,data):
        X = preprocess_and_add_data(data)
        prediction = self.clf.predict(X)
        return prediction
        #based on training will predict delay of locomotive next day




def preprocess_and_add_data(data):
    df = pd.read_csv('.data.csv')
    df.fillna(value=0, inplace=True)
    columns = df.columns.values
    index = 0
    for column in columns[1:2]:
        X = df[column]
        for i, x in enumerate(X):
            if x != 'Late' and x != 'Before':
                index = i
                break
    X = None
    for column in columns[:1]:
        X = df[column][index]
        break
    new_time = str(datetime.datetime.now())
    X = list(X)
    new_time = list(new_time)
    X[:11] = new_time[:11]
    X = "".join(X)
    data_dict = {
        'StartedOn':[X],
        'Delay':df['Delay'][random.randint(0,len(df))]
    }
    enc = LabelEncoder()
    new_df = pd.DataFrame(data=data_dict)
    new_df = new_df.apply((LabelEncoder().fit_transform))
    return new_df

def Get_UserData():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Abhishek-9c1b3fd4771a.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("train-data").sheet1
    ind = (len(sheet.get_all_values()))
    return ((sheet.row_values(ind))[:2])

if __name__=="__main__":
    n = Neon_Engine()
    l = Get_UserData()
    print l[0]
    print l[1]
    n.getdata_and_train(l[0])
    print(n.predict_delay(l[1]))