import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot#değişen değeri çizmek için

cap = cv2.VideoCapture(0)#Video tanımlıyoruz
detector = FaceMeshDetector(maxFaces=1)#Tek yüz tanımı yaptık
plotY=LivePlot(640,360,[20,50],interval=True)#interval grafik çok aşağıda olmaması için


idList=[22,23,24,26,110,157,158,159,160,161,130,243]#findFaceMEsh de elde ettiğimiz faces noktalarını numaralandırarak göz kıpma anlaşılsın istiyoruz
ratioList=[]
ratioEyeList=[]
blinkCounter=0
counter=0
color=(255,0,255)


while True:#Video devamlı çalışabilmesi için true veriyoruz
    #Toplam kaç kare olduğunu kontrol edeceğiz.Toplam kare o anki kareye eşitse sıfırlayacak
    #Devamlılık
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()#görüntüyü yazdırıp eşitliyoruz
    img,faces = detector.findFaceMesh(img,draw=False)#468 noktayı yüz çıkıntılarına yerleştiriyor
    #Göz hizası siyah şekilde belirgin olur.
    if faces:#NOKTARIN HANGİLERİNİN GÖZ HİZASINDA OLDUĞUNU BULMAK İÇİN
        face=faces[0]
        for id in idList:
            cv2.circle(img,face[id],5,color,cv2.FILLED)
        leftUp=face[159]
        leftDown=face[23]
        leftLeft=face[130]
        leftRight=face[243]
        lenghtVer, _= detector.findDistance(leftUp, leftDown)#Gçz üstü ve altı arazında Mesafesi
        lenght, _ = detector.findDistance(leftLeft, leftRight)#yatay çzigi
        cv2.line(img, leftUp, leftDown, (0,200,0), 1)
        cv2.line(img, leftLeft, leftRight, (0,200,0), 2)

        ratio = int((lenghtVer/lenght)*100)#yatay ve dikey oranı
        print(ratio)
        ratioList.append(ratio)
        ratioEyeList.append(ratio)
        if len(ratioEyeList)>20:
            ratioEyeList.pop(0)
        ratioEyeList_Avg=sum(ratioEyeList)/len(ratioEyeList)
        if ratioEyeList_Avg<28:
            cvzone.putTextRect(img, f"Goz kapali", (100, 200), colorR=(255,0,0))
        if ratioEyeList_Avg>29 and ratioEyeList_Avg<32:
            cvzone.putTextRect(img, f"Yorgunluk", (100, 200), colorR=(255,0,0))

        if len(ratioList)>5:#Ortalama oranı vermesi lazım son 5 elemanı
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)

        if ratioAvg < 32 and counter == 0:#göz kırptığı an
            blinkCounter += 1
            color=(0,200,0)
            counter = 1
        if counter!=0:#Köp kapalıyken artmaya başlayacak
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        cvzone.putTextRect(img,f"Goz kirpma Sayisi{blinkCounter}", (50, 100),colorR=color)
        imgPlot = plotY.update(ratioAvg,color)
        img = cv2.resize(img, (640, 360))#video tanımı,dsize boyutlandırma
        imgStack = cvzone.stackImages([img,imgPlot],2,1)


    else:
        img=cv2.resize(img,(640,360))
        imgStack=cvzone.stackImages([img,img],2,1)

    cv2.imshow('Image', imgStack)
    cv2.waitKey(25)#Milisaniye gecikme veriyoruz.