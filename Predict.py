from Explore import *
confirmed_cases = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv')
recoveries = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_recoveries.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv')

cases_58 = confirmed_cases['total'][-58:]
recoveries_58 = recoveries['total'][-58:]
deaths_58 = deaths['total'][-58:]

cases_np = np.array(cases_58)
recoveries_np = np.array(recoveries_58)
deaths_np = np.array(deaths_58)

population = 60695788

def data_spilt(data, orders, start):
    x_train = np.empty((len(data) - start - orders, orders))
    y_train = data[start + orders:]

    for i in range(len(data) - start - orders):
        x_train[i] = data[i + start:start + orders + i]

    # Exclude the day (Feb. 12, 2020) of the change of the definition of confirmed cases in Hubei China.
    x_train = np.delete(x_train, np.s_[28 - (orders + 1) - start:28 - start], 0)
    y_train = np.delete(y_train, np.s_[28 - (orders + 1) - start:28 - start])

    return x_train, y_train

def ridge(x, y):
    print('\nStart searching good parameters for the task...')
    parameters = {'alpha': np.arange(0, 0.100005, 0.000005).tolist(),
                  "tol": [1e-8],
                  'fit_intercept': [True, False],
                  'normalize': [True, False]}

    clf = GridSearchCV(Ridge(), parameters, n_jobs=-1, cv=5)
    clf.fit(x, y)

    print('\nResults for the parameters grid search:')
    print('Model:', clf.best_estimator_)
    print('Score:', clf.best_score_)

    return clf

def predict_page():
    X = cases_np[:] - recoveries_np[:] - deaths_np[:]
    R = recoveries_np[:] + deaths_np[:]

    n = np.array([population] * len(X), dtype=np.float64)

    S = n - X - R

    X_diff = np.array([X[:-1], X[1:]], dtype=np.float64).T
    R_diff = np.array([R[:-1], R[1:]], dtype=np.float64).T

    gamma = (R[1:] - R[:-1]) / X[:-1]
    beta = n[:-1] * (X[1:] - X[:-1] + R[1:] - R[:-1]) / (X[:-1] * (n[:-1] - X[:-1] - R[:-1]))
    R0 = beta / gamma

    from sklearn.linear_model import Ridge
    orders_beta = 3
    orders_gamma = 3

    ##### Select a starting day for the data training in the ridge regression. #####
    start_beta = 10
    start_gamma = 10

    ########## Print Info ##########
    st.write("\nThe latest transmission rate beta of SIR model:", beta[-1])
    st.write("The latest recovering rate gamma of SIR model:", gamma[-1])
    st.write("The latest basic reproduction number R0:", R0[-1])

    ##### Split the data to the training set and testing set #####
    x_beta, y_beta = data_spilt(beta, orders_beta, start_beta)
    x_gamma, y_gamma = data_spilt(gamma, orders_gamma, start_gamma)

    ##### Training and Testing #####
    clf_beta = Ridge(alpha=0.003765, copy_X=True, fit_intercept=False, max_iter=None, normalize=True, random_state=None, solver='auto', tol=1e-08).fit(x_beta, y_beta)
    clf_gamma = Ridge(alpha=0.001675, copy_X=True, fit_intercept=False, max_iter=None,normalize=True, random_state=None, solver='auto', tol=1e-08).fit(x_gamma, y_gamma)

    beta_hat = clf_beta.predict(x_beta)
    gamma_hat = clf_gamma.predict(x_gamma)
    ##### Parameters for the Time-dependent SIR model #####
    stop_X = 0 # stopping criteria
    stop_day = 100 # maximum iteration days 

    day_count = 0
    turning_point = 0

    S_predict = [S[-1]]
    X_predict = [X[-1]]
    R_predict = [R[-1]]

    predict_beta = np.array(beta[-orders_beta:]).tolist()
    predict_gamma = np.array(gamma[-orders_gamma:]).tolist()
    while (X_predict[-1] >= stop_X) and (day_count <= stop_day):
        if predict_beta[-1] > predict_gamma[-1]:
            turning_point += 1

        next_beta = clf_beta.predict(np.asarray([predict_beta[-orders_beta:]]))[0]
        next_gamma = clf_gamma.predict(np.asarray([predict_gamma[-orders_gamma:]]))[0]

        if next_beta < 0:
            next_beta = 0
        if next_gamma < 0:
            next_gamma = 0

        predict_beta.append(next_beta)
        predict_gamma.append(next_gamma)
    
    

        next_S = ((-predict_beta[-1] * S_predict[-1] *
               X_predict[-1]) / n[-1]) + S_predict[-1]
        next_X = ((predict_beta[-1] * S_predict[-1] * X_predict[-1]) /
              n[-1]) - (predict_gamma[-1] * X_predict[-1]) + X_predict[-1]
        next_R = (predict_gamma[-1] * X_predict[-1]) + R_predict[-1]

        S_predict.append(next_S)
        X_predict.append(next_X)
        R_predict.append(next_R)

        day_count += 1
        

    if st.button('Predict'):
        st.write('\nConfirmed cases tomorrow:', np.rint(X_predict[1] + R_predict[1]))
        st.write('Infected persons tomorrow:', np.rint(X_predict[1]))
        st.write('Recovered + Death persons tomorrow:', np.rint(R_predict[1]))
        
        # 0 - today => 7 (weeks)
        for i in range(1,8):
            st.write(f" Day {i}'s cases prediction : {np.rint(X_predict[i] + R_predict[i]) -  np.rint(X_predict[i-1] + R_predict[i-1])}")

        Days = []
        for i in range(1,7):
            Days.append(i)


        Predictions = []
        for i in range(1,7):
            Predictions.append({np.rint(X_predict[i] + R_predict[i]) -  np.rint(X_predict[i-1] + R_predict[i-1])})

        
        









