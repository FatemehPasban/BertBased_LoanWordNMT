import pandas as pd


def stat_after_split(test_s_ids, val_s_ids, train_s_ids, loan_words_stat, df_data, new_100_selected_loans):

    sent_id_to_loanslist = dict(zip(df_data[0].values, df_data[3].apply(eval)))

    # تعداد تکرار هر وام واژه در داده های تست
    test_loan_stat = {}
    for sent_id in test_s_ids:
        for loan in sent_id_to_loanslist[sent_id]:
            if loan in new_100_selected_loans.values:
                if loan in test_loan_stat.keys():
                    test_loan_stat[loan][0] = test_loan_stat[loan][0] + 1
                    test_loan_stat[loan][1] = test_loan_stat[loan][1] + [sent_id]
                else:
                    test_loan_stat[loan] = [1, [sent_id]]

    # تعداد تکرار هر وام واژه در داده های ولید
    val_loan_stat = {}
    for sent_id in val_s_ids:
        for loan in sent_id_to_loanslist[sent_id]:
            if loan in new_100_selected_loans.values:
                if loan in val_loan_stat.keys():
                    val_loan_stat[loan][0] = val_loan_stat[loan][0] + 1
                    val_loan_stat[loan][1] = val_loan_stat[loan][1] + [sent_id]
                else:
                    val_loan_stat[loan] = [1, [sent_id]]

    # تعداد تکرار هر وام واژه در داده های ترین
    train_loan_stat = {}
    for sent_id in train_s_ids:
        for loan in sent_id_to_loanslist[sent_id]:
            if loan in new_100_selected_loans.values:
                if loan in train_loan_stat.keys():
                    train_loan_stat[loan][0] = train_loan_stat[loan][0] + 1
                    train_loan_stat[loan][1] = train_loan_stat[loan][1] + [sent_id]
                else:
                    train_loan_stat[loan] = [1, [sent_id]]
    # اضافه کردن آمار تکرار وام واژه‌ها در داده های تست و ترین به امار کلی وام واژه ها
    # هر وام واژه چندتا تکرار داشته | توی چه جمله هایی ظاهر شده | تعداد تکرارش در تست | تعدا تکرارش در ترین
    for loan in loan_words_stat.keys():
        test_rep = test_loan_stat[loan] if test_loan_stat.get(loan) else [0, []]
        val_rep = val_loan_stat[loan] if val_loan_stat.get(loan) else [0, []]
        train_rep = train_loan_stat[loan] if train_loan_stat.get(loan) else [0, []]
        loan_words_stat[loan] = loan_words_stat[loan] + test_rep + val_rep + train_rep
    #  مشخص میکنه از هر لوین چندتا داریم | توی کدوم جمله ها | توی مجموعه تست چندتا داریم | توی مجموعه ترین چندتا داریم
    #  اعتماد |  14  |  [12, 543, 78, ...] | 3 | 11
    df_stat_after_split = pd.DataFrame.from_dict(loan_words_stat, orient="index", columns=["total_rep", "sent_ids", "test_rep", "test_sent_ids", "val_rep", "val_sent_ids", "train_rep", "train_sent_ids"])
    # df_stat_after_split = pd.DataFrame.from_dict(loan_words_stat, orient="index")
    df_stat_after_split.to_csv("../../data/preprocessed_data/created_raw_files/stat/train_test_val_rep_stat.csv")
    print("train_test_val_rep_stat.csv created")
