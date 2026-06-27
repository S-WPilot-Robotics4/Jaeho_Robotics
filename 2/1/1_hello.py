import os

# 생성할 디렉토리와 파일 경로 설정
dir_path = "/test"
file_path = os.path.join(dir_path, "hello.txt")

try:
    # /test 디렉토리가 없으면 생성
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 파일에 문자열 작성 (w 모드: 덮어쓰기)
    with open(file_path, "w") as f:
        f.write("Hello Linux")

    print(f"[성공] '{file_path}' 파일이 생성되었으며, 'Hello Linux'가 정상적으로 작성되었습니다.")

except PermissionError:
    print("[에러] 권한이 거부되었습니다. 관리자 권한(sudo)으로 실행해주세요.")
except Exception as e:
    print(f"[에러] 알 수 없는 오류 발생: {e}")