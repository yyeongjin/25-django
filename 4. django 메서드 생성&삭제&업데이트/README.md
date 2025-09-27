# Django POST 메서드: 생성 및 삭제 구현 + 업데이트 구현

## 1. POST 메서드로 데이터 생성

`views.py`에서 `create` 함수 작성:

```python
def create(request):
    num_model = demo_model()
    num_model.num = request.POST.get('num')
    num_model.destination = request.POST.get('destination')
    num_model.save()
    return redirect('articles:index')
```

- `redirect`를 통해 데이터 생성 후 `index` 페이지로 이동

![views 정의](images/image-3.png)

`urls.py`에 path와 app_name 추가:

![urls 설정](images/image-1.png)

---

## 2. 데이터 생성 폼 추가

`index.html` 안에 해당 내용을 포함합니다.

```html
<form action="{% url 'articles:create' %}" method="POST">
    {% csrf_token %}
    <label for="num">num : </label>
    <input type="text" id="num" name="num">
    <br>
    <label for="content">destination: </label>
    <input type="text" id="destination" name="destination">
    <br>
    <button type="submit">제출</button>
</form>
```

- CSRF 토큰 필수
- 폼 제출 시 `create` 뷰를 호출합니다.

![alt text](images/image-2.png)

---

## 3. 데이터 삭제 구현

`views.py`에서 `delete` 함수 작성:

```python
def delete(request, num):
    num_model = demo_model.objects.filter(id=num)
    num_model.delete()
    return redirect('articles:index')
```

`urls.py`에 삭제 경로 추가:

```python
path('delete/<int:num>/', delete, name="delete"),
```

![urls delete 추가](images/image-4.png)

---

## 4. 삭제 버튼 추가

`num.html`에 삭제 버튼 폼 작성:

```html
{% extends "base.html" %}
{% block content %}
{% for value in num %}
<p>{{ value.id }}</p>
<p>{{ value.num }}</p>
<p>{{ value.destination }}</p>
<form action="{% url 'articles:delete' value.id %}" method="POST">
    {% csrf_token %}
    <button type="submit">삭제</button>
</form>
{% endfor %}
{% endblock content %}
```

- 각 데이터 항목마다 삭제 버튼 생성
- POST 메서드 사용 및 CSRF 토큰 포함

---

## 5. 서버 실행 및 확인

```bash
python manage.py runserver
```

- 정상적으로 생성 및 삭제 기능 동작 확인 가능

![생성 테스트](images/image-5.png)
![게시물 접속 테스트](images/image-6.png)
![삭제 테스트](images/image-7.png)
![삭제 확인](images/image-8.png)

---

## 6. 데이터 업데이트 구현

### 1) `articles/urls.py` 수정
먼저 `articles` 앱의 URL 설정에 `update` 경로를 추가해야 합니다.

```python
    path('update/<int:num>/', update, name="update"),
```
![update URL 추가](images/update-image.png)

---

### 2) `articles/views.py` 수정
`update` 요청을 처리할 뷰 함수를 추가합니다.  
이 함수는 **GET 요청 시 수정할 데이터를 보여주고, POST 요청 시 데이터를 업데이트**합니다.

```python
def update(request, num):
    num_model = demo_model.objects.get(id=num)

    if request.method == 'POST':
        num_model.num = request.POST.get('num')
        num_model.destination = request.POST.get('destination')
        num_model.save()
        return redirect('articles:num', num=num_model.id)
    else:
        context = {
            'num': num_model,
        }
        return render(request, 'update.html', context)
```

![views 추가](images/update-image-1.png)

---

### 3) `articles/templates/update.html` 생성
데이터를 수정할 수 있는 폼이 있는 새로운 HTML 파일을 생성합니다.

```html
{% extends "base.html" %}

{% block content %}
  <h1>게시글 수정</h1>
  <form action="{% url 'articles:update' num.id %}" method="POST">
    {% csrf_token %}
    <label for="num">num : </label>
    <input type="text" id="num" name="num">
    <br>
    <label for="content">destination: </label>
    <input type="text" id="destination" name="destination">
    <br>
    <button type="submit">제출</button>
  </form>
{% endblock content %}
```

---

### 4) `articles/templates/num.html` 수정
상세 페이지(`num.html`)에서 수정 페이지로 이동할 수 있는 링크를 추가합니다.

```html
{% extends "base.html" %}
{% block content %}
{% for value in num %}
<p>{{ value.id }}</p>
<p>{{ value.num }}</p>
<p>{{ value.destination }}</p>

<a href="{% url 'articles:update' value.id %}">수정하기</a>
<form action="{% url 'articles:delete' value.id %}" method="POST">
    {% csrf_token %}
    <button type="submit">삭제</button>
</form>
{% endfor %}
{% endblock content %}
```
![num 페이지 수정](images/update-image-2.png)

### 5). 서버 실행 및 확인

```bash
python manage.py runserver
```

- 정상적으로 업데이트 동작 확인 가능

![게시글 선택](images/update-image-3.png)
![게시글 수정 선택](images/update-image-4.png)
![게시글 수정하기](images/update-image-5.png)
![업데이트 확인](images/update-image-6.png)