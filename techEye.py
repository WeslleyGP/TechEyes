from gtts import gTTS
import os
import speech_recognition as sr
import cv2
import pytesseract

def camera():
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame = cap.read()
    
        cv2.imshow("WebCam",frame)
    
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
def lerEmbalagem():
    # Inicializa a captura de vídeo
    cap = cv2.VideoCapture(0)

    # Verifica se a câmera foi aberta corretamente
    if not cap.isOpened():
        print("Não foi possível abrir a câmera.")
        return

    # Captura o frame
    ret, frame = cap.read()

    # Verifica se o frame foi capturado corretamente
    if not ret:
        print("Não foi possível capturar o frame.")
        return
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    
    # Salva o frame como imagem PNG
    cv2.imwrite("frame.png",frame_gray )

    # Libera a câmera
    cap.release()

    # Imagem -> Texto
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Caminho para o executável do Tesseract no Linux/Unix

    rotulo = pytesseract.image_to_string('frame1.png')

    print("Texto reconhecido:")
    print(rotulo.split()[0])
    return rotulo.split()[0]

def converterVoz(texto, lang='pt-br'):
    tts = gTTS(text=texto, lang=lang)
    tts.save("output.mp3")
    os.system("vlc --play-and-exit output.mp3")


def comandoVoz():
    mic = sr.Recognizer()

    with sr.Microphone() as barulho:
        mic.adjust_for_ambient_noise(barulho)
        converterVoz('Em que posso ajudar?')
        print("Diga algo...")
        
        
           
        
        try:
            
            audio = mic.listen(barulho)
            voz = mic.recognize_google(audio, language='pt-BR')
            converterVoz('Escaneando....')
            
            
        except sr.UnknownValueError:
            print("Não foi possível reconhecer o áudio")

        except sr.RequestError as e:
            print("Erro na requisição ao serviço de reconhecimento de fala:", str(e))
            
        comando = ''
        
        if 'objeto' in voz:
            comando = camera()
        
        elif 'embalagem' in voz:
            comando = lerEmbalagem()
        
        else:
            comando = ('comando não encontrado')
            
        
        return converterVoz(comando)
            
        

comandoVoz()
