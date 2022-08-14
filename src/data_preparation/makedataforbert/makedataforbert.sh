#!/usr/bin/env bash
#lng="de"
lng="pa"
#path = "/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/"

echo "src lng $lng"
for sub  in train valid test
do
    sed -r 's/(@@ )|(@@ ?$)//g' ${/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/}${sub}.${lng} > ${/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/}${sub}.bert.${lng}.tok
    ./detokenizer.perl -l $lng < ${/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/}${sub}.bert.${lng}.tok > ${/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/}${sub}.bert.${lng}
    rm ${/home/fatemeh/PycharmProjects/BertBased_LoanWordNMT/data/preprocessed_data/created_raw_files/}${sub}.bert.${lng}.tok
done