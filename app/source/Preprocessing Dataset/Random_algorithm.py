#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
#print("Content-Type: text/html\n")
import random
import utils
import statistics

def random_algorithm(x_train, x_test, number_of_total_instances, number_of_quantum_training_instances, number_of_evaluations=100):
    acc=[]
    for i in range(number_of_evaluations):
        list_of_instances = list([random.randint(0, number_of_total_instances-1) for p in range(number_of_quantum_training_instances)])
        acc.append(utils.test(x_train, x_test, list_of_instances))

    return statistics.median_high(acc)

