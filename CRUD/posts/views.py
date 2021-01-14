from .forms import PostForm
from .models import Post
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here


def post_list(request):
    '''
    Retrieve, Read == SELECT
    저장된 모든 포스트를 렌더링하는 뷰
    '''
    posts = Post.objects.all()  # 정확히는 여기가 Retrieve(Read)
    ctx = {'posts': posts}

    return render(request, template_name='posts/list.html', context=ctx)


def post_detail(request, post_id):
    '''
    Retrieve, Read == SELECT
    url 파라미터로 가져온 post_id(pk)에 해당하는 특정 포스트만을 렌더링하는 뷰
    '''
    # print(pk) # -> url에서 넘겨준 parameter

    post = Post.objects.get(id=post_id)  # 정확히는 여기가 Retrieve(Read)
    # post = get_object_or_404(Post, id=pk) # get과 같은 역할을 수행하지만, 해당하는 객체를 못찾으면 404에러를 띄운다
    # 안정성 측면에서 get_object_or_404를 사용하는것이 더 선호된다.

    # print(dir(post)) # -> post의 내부 변수들을 보여준다
    # print(post.id) # -> 해당 post의 id는 (당연히) pk와 같다.
    ctx = {'post': post}

    return render(request, template_name='posts/detail.html', context=ctx)


def create_post(request):
    '''
    Create == INSERT
    모델과 폼을 이용하여 새로운 인스턴스를 생성하고 DB에 저장하는 뷰
    GET방식과 POST 방식의 차이에 대해 반드시 학습할것!
    '''
    if request.method == 'POST':
        # print(request.POST) # 유저가 POST로 보내온 정보를 확인할 수 있다.
        form = PostForm(request.POST)  # 유저가 전송해온 데이터(POST)를 채워넣은 form객체 생성
        if form.is_valid():  # form의 각 필드에 대하여 유효성 검증
            post = form.save()  # DB에 저장
            return redirect('posts:list')
    else:  # 일반적으로 GET방식
        form = PostForm()
        ctx = {'form': form}

        return render(request, 'posts/post_form.html', ctx)


def update_post(request, post_id):
    '''
    Update == UPDATE
    DB에 저장된 객체를 다시 form형태로 불러와 수정하고, 재저장하는 뷰
    '''
    post = get_object_or_404(
        Post, pk=post_id)  # detail의 id와 여기의 pk는 동일하게 객체의 인덱스를 나타냅니다.

    if request.method == 'POST':
        # instance=post는 특정 instance(여기서는 위에서 가져온 post)에 대한 form임을 나타냄.
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()

            # url 파라미터를 이렇게 넘겨줄 수 있습니다.
            return redirect('posts:detail', post_id=post.id)

    else:  # 일반적으로 GET 방식
        form = PostForm(instance=post)
        ctx = {'form': form}
        return render(request, 'posts/post_form.html', ctx)


def delete_post(request, post_id):
    '''
    delete == DELETE
    DB에 저장된 객체를 불러와 삭제하는 뷰
    '''
    post = get_object_or_404(Post, id=post_id)

    # 유저가 주소창에에 delete의 url를 직접 쳐서 들어오는 경우를 고려하여 GET처리를 해준다
    if request.method == "GET":
        return redirect('posts:detail', post_id)
    elif request.method == "POST":
        post.delete()
        return redirect('posts:list')

    # GET과 POST의 순서는 이런식으로 바뀌어도 상관없습니다.
    # 단, 사용자가 GET과 POST방식으로만 접근한다는 보장은 없으므로, 이외의 method를 사용 시 오류가 날 수 있습니다.
