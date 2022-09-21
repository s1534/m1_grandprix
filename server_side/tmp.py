from collections import deque

b = [0] *15
eval_json = {
    "evals" :[
        0,20,40,60,80,100
    ]
}


a = deque(b)

a.append(1)

eval_json["evals"] = list(a)

print(eval_json)