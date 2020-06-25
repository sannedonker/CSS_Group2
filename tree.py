from plot import make_df
from sklearn.model_selection import KFold


make_df(data = pickle.load(open('output\\RUN_DATA_most_random.p', 'rb')))

X = df.iloc[:,5:].values
y = np.array([ int(i) if i == i else 0 for i in df['moment'].values * 20 ])

kf = KFold(n_splits=5)
kf.get_n_splits(X)

s = []
for train_index, test_index in kf.split(X):
    train_x = X[train_index]
    test_x = X[test_index]

    train_y = y[train_index]
    test_y = y[test_index]

    from sklearn.tree import DecisionTreeClassifier
    DT = DecisionTreeClassifier()
    result = DT.fit(train_x, train_y)


    y_pred = result.predict(test_x)

    error = 0
    for i,j in zip(y_pred, test_y):
        error += abs(i * 0.05 - j * 0.05)

    s.append(error/len(y_pred))


def sorty(x):
    return x[0]


l = list(zip(DT.feature_importances_, names[5:]))
l.sort(key=sorty)

v, imp = zip(*l)

print('Error (std)', sum(s)/5,"(", np.std(s), ")")
print('least, to most important:', imp)