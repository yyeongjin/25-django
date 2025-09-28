## Django Form과 ModelForm

### Form (`forms.Form`)
- 데이터 입력을 받기 위한 **독립적인 폼 클래스**
- DB와는 직접 연결되지 않음
- 입력값 검증(`is_valid()`) 후 `cleaned_data`에서 값 사용
- DB 저장이 필요 없는 경우(검색, 글자 수 계산 등) 활용

### ModelForm (`forms.ModelForm`)
- 특정 **모델과 연결**된 폼 클래스
- 모델 필드 기반으로 자동 폼 필드 생성
- `form.save()`를 통해 DB 저장 가능
- 모델 제약조건 + 폼 유효성 검사 동시 수행
- 게시글 작성, 댓글 작성 등 **DB 저장이 필요한 입력**에 활용

---

## forms 사용하기

### 1. articles/forms.py 생성  
```python
from django import forms

class TextForm(forms.Form):
    text = forms.CharField(
        label="텍스트 입력",
        widget=forms.TextInput(attrs={'placeholder': '여기에 입력하세요'})
    )
```
![forms 생성](images/image.png)

### 2. views.py 수정  

is_valid: 유효성 검사 체크 함수
```python
from django.shortcuts import render
from .forms import TextForm
from .models import demo_model

def index(request):
    num_model = demo_model.objects.all()
    result = None

    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            result = len(text)
    else:
        form = TextForm()

    context = {
        "num": num_model,
        "form": form,
        "result": result
    }
    return render(request, 'index.html', context)
```
![views 수정](images/image-1.png)

### 3. index.html 템플릿 

기존 {% endblock content %} 위에 해당된 내용 추가합니다.
```django
<br>
<hr>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="글자 수 조회하기">
    <p>입력한 글자의 수는 <b>{{ result }}</b> 입니다.</p>
</form>
```
![html 수정](images/image-2.png)

## 4. 서버 실행 및 확인

```bash
python manage.py runserver
```

![글자 입력](images/image-3.png)
![글자 수 조회 화면](images/image-4.png)


---

## ModelForm 사용하기
### 1. forms.py에서 Modelform 정의 (demo_model 상속)
```python
from .models import demo_model

class DemoForm(forms.ModelForm):
    class Meta:
        model = demo_model
        fields = '__all__' # 포함하다
        # 이런식으로도 쓰일 수 있음 ('num','destination',)
        # exclude의 경우는 제외하다
```
![modelform 정의](images/image-5.png)

### 2. create 함수 주석 처리
![create 함수 주석](images/image-10.png)
![create 함수 주석](images/image-11.png)



## articles/views.py index 함수 수정
create 함수없이 index에서 처리합니다.
```python
from .forms import TextForm, DemoForm

def index(request):
    num_model = demo_model.objects.all()
    result = None
    if request.method == "POST":
        form = TextForm(request.POST)
        demo_form = DemoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            result = len(text)
        if demo_form.is_valid():
            demo_form.save()
            return redirect('articles:index')
    else:
        form = TextForm()
        demo_form = DemoForm()

    context = {
        "num": num_model,
        "form": form,
        "result": result,
        'demo_form': demo_form
    }
    return render(request, 'index.html', context)
```
![views 함수 수정](images/image-12.png)

## articles/index.html 수정

![제거할 구문](images/image-8.png)
![추가할 구문](images/image-13.png)


## 3. 서버 실행 및 확인

```bash
python manage.py runserver
```
![적용 확인](images/image-14.png)
![생성하기](images/image-15.png)
![조회하기](images/image-16.png)


## 4. 트러블 슈팅
텍스트 입력 후 조회 시도 시, 유효성 검사가 동시에 발생하는 문제점이 있음
![텍스트 조회하기](images/image-17.png)
![결과 화면](images/image-18.png)

views.py에서 index 함수 수정
```python
def index(request):
    num_model = demo_model.objects.all()
    result = None
    form = TextForm()
    demo_form = DemoForm()

    if request.method == "POST":
        if 'form' in request.POST:
            form = TextForm(request.POST)
            if form.is_valid():
                result = len(form.cleaned_data['text'])
        elif 'demo_form' in request.POST:
            demo_form = DemoForm(request.POST)
            if demo_form.is_valid():
                demo_form.save()
                return redirect('articles:index')

    context = {
        "num": num_model,
        "form": form,
        "result": result,
        "demo_form": demo_form
    }
    return render(request, 'index.html', context)
```

index.html에서 제출 시 name 추가
![index.html 수정](images/image-19.png)

## 서버 실행 및 확인

```bash
python manage.py runserver
```
![텍스트 길이 조회](images/image-20.png)
![길이 출력](images/image-21.png)
