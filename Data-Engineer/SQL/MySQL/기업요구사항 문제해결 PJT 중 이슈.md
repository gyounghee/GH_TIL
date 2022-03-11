* OSError: cannot write mode RGBA as JPEG
 - jpg파일은 투명도를 표현할 수 없는 파일 포멧인데 여기에 alpha값을 저장하려고 할 경우 발생되는 에러
 - 해결방법
    - im = im.convert("RGB")
    - im.save('python.jpg')