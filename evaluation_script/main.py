import sys
import traceback


def prepareUsersAnnotation(file):
    with open(file, "r") as f:
        text = f.readlines()
    res = []

    for line in text:
            line = line.rstrip('\n') # remove \n at the end of line
            items = line.split(',')
            # change array/list to tuple
            items[1] = items[1].split(' ')
            res.append(tuple(items))
    return res

def prepareTestsAnnotation(file):
    with open(file, "r") as f:
        text = f.readlines()
    res = dict()

    for line in text:
            line = line.rstrip('\n') # remove \n at the end of line
            items = line.split(',')
            res[items[0]] = items[1].split(' ')
    return res


def evaluate(test_annotation_file ,user_annotation_file, phase_codename, **kwargs):

    tests = prepareTestsAnnotation(test_annotation_file)
    users = prepareUsersAnnotation(user_annotation_file)

    # Delete Header
    tests.pop('User')
    users.pop(0)

    numberOfUserAnnotationRows = len(users)
    averagePrecision = 0
    meanAveragePrecision = 0
    for u in range(1,numberOfUserAnnotationRows + 1):

        if users[u-1][0] not in tests:
            continue

        m = len(tests.get(users[u - 1][0]))
        n = len(users[u - 1][1])
        precisionAtK = 0

        for k in range(1, min(n, 200) + 1):
            relevant = 0
            kth = False
            for i in range(k):
                if users[u - 1][1][i] in tests.get(users[u - 1][0]):
                    relevant+=1
                
                if users[u - 1][1][i] in tests.get(users[u - 1][0]) and i == k-1:
                    kth=True

            if kth == True:
                precisionAtK = precisionAtK + (relevant / k)

        averagePrecision = averagePrecision + (precisionAtK / min(m, 200))

    meanAveragePrecision = averagePrecision / max(len(tests), numberOfUserAnnotationRows)

    output = {}

    if phase_codename == "final":
        try:
            output['result'] = [
                {
                    'test_split': { # dataset split codename
                        'Score': meanAveragePrecision,
                    }
                }
            ]
            return output
        except Exception as e:
            sys.stderr.write(traceback.format_exc())
            return e

# print(evaluate("annotation.csv", "user_annotation.csv", phase_codename="final"))