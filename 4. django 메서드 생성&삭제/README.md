# Django POST 메서드: 생성 및 삭제 구현

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