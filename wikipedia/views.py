import requests
from django.shortcuts import render, redirect
from .models import Article, Tag
from langchain import LLMChain
from langchain.prompts import Prompt
from .forms import TagForm  # form to handle tag updates
from django.shortcuts import get_object_or_404

def search_wikipedia(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
        response = requests.get(url)
        data = response.json()
        results = data.get('query', {}).get('search', [])
    
    return render(request, 'search.html', {'results': results, 'query': query})


def generate_tags(article_content):
    prompt = Prompt("Generate relevant tags for this article:")
    llm_chain = LLMChain(prompt=prompt, llm="gemini-pro")
    tags = llm_chain.run({"article_content": article_content})
    return tags

def save_article(request, title, snippet, url):
    article, created = Article.objects.get_or_create(
        user=request.user,
        title=title,
        snippet=snippet,
        url=url
    )

    # Generate tags using LangChain and Gemini Pro
    tag_names = generate_tags(snippet)
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        article.tags.add(tag)
    
    return redirect('saved_articles')

def saved_articles(request):
    articles = Article.objects.filter(user=request.user)
    return render(request, 'saved_articles.html', {'articles': articles})

def edit_tags(request, article_id):
    article = get_object_or_404(Article, id=article_id, user=request.user)
    
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # Clear current tags and add the updated ones
            article.tags.clear()
            for tag_name in form.cleaned_data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)
            return redirect('saved_articles')
    else:
        form = TagForm(initial={'tags': [tag.name for tag in article.tags.all()]})

    return render(request, 'edit_tags.html', {'form': form, 'article': article})
