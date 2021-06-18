from multiprocessing import Process
import time


def meineFunc():
    print("saylalala")
    text = "a"
    text1 = ""
    stepper = 1
    stepper_count = 0

    for i in range(100000000):
        if stepper == 1 and stepper_count < 250:
            text1 += text
            stepper_count += 1
            time.sleep(0.01)

        elif stepper == 1 and stepper_count >= 250:
            stepper = 0

        elif stepper == 0 and stepper_count > 0:
            text1 = text1[:-1]
            stepper_count -= 1
            time.sleep(0.01)
        elif stepper == 0 and stepper_count <= 0:
            stepper = 1
            text1 = "pisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpisswegpissweg"


        print(text1)
    print("saylalala end")


if __name__ == '__main__':


    process1 = Process(target=meineFunc())
    process2 = Process(target=meineFunc())

    process1.start()
    #process2.start()



    print("wuhahahaha")