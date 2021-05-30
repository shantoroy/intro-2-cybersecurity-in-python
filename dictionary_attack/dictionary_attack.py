#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   problem_2.py
@Time    :   2021/05/28 23:27:16
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@License :   Free to use/modify/share
@Desc    :   None
'''


import pandas as pd
from hashlib import sha256
import time
import itertools 
import collections

# read all three files using pandas.read_csv
dictionary = pd.read_csv("password_dictionary", names=['passwords'])
users = pd.read_csv("users")
users_salted = pd.read_csv("users_salted")


# inputs an string and returns the sha256 digest
def create_hash(word):
    pass_bytes = word.encode('utf-8')
    pass_hash = sha256(pass_bytes)
    digest = pass_hash.hexdigest()
    return digest


# inputs an string and returns the salted (salt+pass) sha256 digest
def salted_hash(salt,password):
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    hashed_password = sha256(salt+password).hexdigest()
    return hashed_password
        

# inputs the number of users and returns nothing
# intended for finding passwords for multiple users
def find_multiple_users(num_user):
    for i in range(num_user):
        check_pass = users["password_hash"][i]
        for test_word in dictionary["passwords"]:
            if create_hash(test_word) == check_pass:
                break
                

# Returns the dictionary of password and corresponding digests
def hash_dictionary():
    global hash_dict
    hash_dict = {}
    for test_word in dictionary["passwords"]:
        hash_dict[test_word] = create_hash(test_word)
    return hash_dict

# # assign the hash dictionary in a variable
# hash_dict = hash_dictionary()



#################### PROBLEMS and SOLUTIONS #####################

def experiment_1():
    print("Experiment 1: Time taken to match a dictionary word for\n the first user)")
    check_pass = users["password_hash"][0]
    start = time.time()
    for test_word in dictionary["passwords"]:
        if create_hash(test_word) == check_pass:
            print("Matched Password:", test_word)
            break
    stop = time.time()
    print('Time (Approx) taken for the first user: {:.2f} seconds'.format(stop - start))
    print("")
    


def experiment_2():
    print("Experiment 2: Approximate Avg. time for all users")
    n = 10
    start = time.time()
    find_multiple_users(n)
    stop = time.time()
    avg_time = (stop - start)/n
    print("Average time (Approx) taken for one user: {:.2f}".format(avg_time))
    total_time = avg_time * len(users) / 3600
    print("Estimated Total Time (Approx): {:.2f} Hours".format(total_time))
    print("")
    
    print("Estimation based on Dictionary Size")
    print("Estimated Total Time (Approx): {:.2f} Years".format(total_time*(62 ** 8)/len(dictionary)/24/365))
    print("")
    


def experiment_3(hash_dict):
    print("Experiment 3: approx time if used the Hash dictionary (precomputed hash)")
    check_pass = users["password_hash"][0]
    start = time.time()
    for key in hash_dict:
        if hash_dict[key] == check_pass:
            print("Matched Password:", key)
            break
    stop = time.time()
    print('Time (Approx) taken for the first user: {:.2f} seconds'.format(stop - start))
    print("")
    


def experiment_4():
    print("Experiment 4: Adding Salt to user password to avoid duplicates")
    
    # find all duplicate passwords from 'users' file
    duplicate_pass = [item for item, count in collections.Counter(users["password_hash"]).items() if count > 1]
    
    # find usernames of first duplicate password
    find_users = users[users["password_hash"] == duplicate_pass[0]]["username"].tolist()
    
    # show that passwords are same for two users but not same for the salted ones
    print("Password of user:", find_users[0], "->")
    print(users[users["username"] == find_users[0]]["password_hash"].tolist()[0])
    print("Password of user:", find_users[1], "->")
    print(users[users["username"] == find_users[1]]["password_hash"].tolist()[0])
    print("")
    
    # get the salted password hash from users_salted dataframe
    user1_salted_hash = users_salted[users_salted["username"] == find_users[0]]["password_hash"].tolist()[0]
    user2_salted_hash = users_salted[users_salted["username"] == find_users[1]]["password_hash"].tolist()[0]
    print("Salted Password of user:", find_users[0], "->")
    print(user1_salted_hash)
    print("Salted Password of user:", find_users[1], "->")
    print(user2_salted_hash)
    if user1_salted_hash != user2_salted_hash:
        print("Salted passwords does not match for both users")
        print("")
    
    
    print("verify salted passwords are correct")
    check_pass = users[users["username"] == find_users[0]]["password_hash"].tolist()[0]
    for test_word in dictionary["passwords"]:
        if create_hash(test_word) == check_pass:
            print("Matched Password for both users:", test_word)
            print("")
            break
    
    # get the salt from users_salted dataframe
    # calculated salted password hash using the "salted_hash" function
    user1_salt = users_salted[users_salted["username"] == find_users[0]]["salt"].tolist()[0]
    user1_calc_salted_hash = salted_hash(user1_salt, test_word)
    user2_salt = users_salted[users_salted["username"] == find_users[1]]["salt"].tolist()[0]
    user2_calc_salted_hash = salted_hash(user2_salt, test_word)
    
    if user1_salted_hash == user1_calc_salted_hash and user2_salted_hash == user2_calc_salted_hash:
        print("Verification is Correct")
        print("Calculated Salted Password of user:", find_users[0], "->")
        print(user1_calc_salted_hash)
        print("Calculated Salted Password of user:", find_users[1], "->")
        print(user2_calc_salted_hash)

        

# main function runs all the problem-solution functions
if __name__ == "__main__":
    hash_dict = hash_dictionary()
    experiment_1()
    experiment_2()
    experiment_3(hash_dict)
    experiment_4()
