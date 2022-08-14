import sqlite3
import pandas as pd
from src.data_preparation import stat_after_split


def split_test_train():
    test_s_ids = []
    val_s_ids = []
    train_s_ids = []
    # برای هر وام واژه ۲۰ درصد از جمله هاشو به تست و بقیه رو به ترین و ولید میدهیم. چون ممکنه یک جمله چندتا وام واژه داشته
    # باشه و در تقسیم بندی یکی از وام واژه ها در داده های تست قرار بگیره ولی در تقسیم بندی هموگراف دیگه در داده های
    # ترین قرار یگیره در اخر لیست ایدی جمله های تست رو از لیست ترین حذف میکنیم
    # ینی برای هر لوین، لیست آیدی جمله هایی که توش ظاهر شده
    for llist in df_stat[1]:
        test_cut = round(len(llist) * 0.2)
        test_s_ids += llist[:test_cut//2]
        val_s_ids += llist[test_cut//2:test_cut]
        train_s_ids += llist[test_cut:]
    test_s_ids = list(set(test_s_ids))
    val_s_ids = list(set(val_s_ids))
    train_s_ids = list(set(train_s_ids))
    val_s_ids = [sid for sid in val_s_ids if sid not in test_s_ids]
    train_s_ids = [sid for sid in train_s_ids if sid not in test_s_ids+val_s_ids]

    # creating train_test_val_rep_stat.csv
    stat_after_split(test_s_ids, val_s_ids, train_s_ids,loan_words_stat, df_data, new_100_selected_loans)
    create_data(test_s_ids, val_s_ids, train_s_ids)


def create_data(test_s_ids, valid_s_ids, train_s_ids):
    sid_to_spair = dict(zip(df_data[0], zip(df_data[1], df_data[2])))
    for data_part in [test_s_ids, valid_s_ids, train_s_ids]:
        part = "test" if data_part == test_s_ids else "valid" if data_part == valid_s_ids else "train"
        part_fa = open(f"../../data/preprocessed_data/created_raw_files/{part}.fa", mode="w")
        part_pa = open(f"../../data/preprocessed_data/created_raw_files/{part}.pa", mode="w")
        for sid in data_part:
            sent = sid_to_spair[sid][0]
            sent_pair = sid_to_spair[sid][1]
            part_fa.write(sent+"\n")
            part_pa.write(sent_pair+"\n")
        part_fa.close()
        part_pa.close()


if __name__ == "__main__":
    new_100_selected_loans = pd.read_excel("/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/new_balance_dict.xlsx")["واژه"]
    con = sqlite3.Connection("/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/loan_dataset.sqlite")
    c = con.cursor()
    df_data = pd.DataFrame(c.execute(
        """
            select sent_id,parallel_data.sent,sent_pair,loan_list from parallel_data 
            inner join sents s on parallel_data.sent_id = s.id 
            where user_id is ? and sent_pair is not ?
        """, ("loan_user2", "Report")
    ))
    sid_to_spair = dict(zip(df_data[0], zip(df_data[1], df_data[2])))
    df_test = pd.DataFrame.from_dict(sid_to_spair, orient="index")
    loan_words_stat = {}
    # {"loan": [rep, [sent_ids]]} => {"اهمیت" : [34,[23, 45, 45, ...]]}
    for sent_id, loan_list in zip(df_data[0].values, df_data[3].apply(eval)):
        for loan in loan_list:
            if loan in new_100_selected_loans.values:
                if loan in loan_words_stat.keys():
                    loan_words_stat[loan][0] = loan_words_stat[loan][0] + 1
                    loan_words_stat[loan][1] = loan_words_stat[loan][1] + [sent_id]
                else:
                    loan_words_stat[loan] = [1, [sent_id]]
    # مشخص میکنه از هر لوین چندتا داریم و توی کدوم جمله ها
    # اعتماد |  14  |  [12, 543, 78, ...]
    df_stat = pd.DataFrame.from_dict(loan_words_stat, orient="index")
    split_test_train()
