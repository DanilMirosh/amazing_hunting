import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from amazing_hunting import settings
from vacancies.models import Vacancy, Skill


def hello(request):
    return HttpResponse("Hello world!")


class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        # СОРТИРОВКА (второй способ через модель)
        self.object_list = self.object_list.order_by("text")
        # self.object_list = self.object_list.order_by("-text")     обратная сортировка

        # """
        # пагинация
        # 1 - 0:10
        # 2 - 10:20
        # 3 - 20:30
        #
        # total = self.object.count()
        # page_number = int(request.GET.get("page", 1))
        # offset = int(page_number - 1) * settings.TOTAL_ON_PAGE
        # if (page_number - 1) * settings.TOTAL_ON_PAGE < total:
        #     self.object_list = self.object_list[offset:offset + settings.TOTAL_ON_PAGE]
        # else:
        #     self.object_list = self.object_list[offset:offset + total]
        # """
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = []
        for vacancy in page_obj:
            vacancies.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })

        response = {
            "items": vacancies,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug,
            "status": vacancy.status,
            "created": vacancy.create,
            "user": vacancy.user_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy.objects.create(
            user_id=vacancy_data["user_id"],
            slug=vacancy_data["slug"],
            text=vacancy_data["text"],
            status=vacancy_data["status"]
        )

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["slug", "text", "status", "skills"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)

        self.object.slug = vacancy_data["slug"]
        self.object.text = vacancy_data["text"]
        self.object.status = vacancy_data["status"]

        for skill in vacancy_data["skills"]:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"error": "skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        list(self.object.skills.all().values_list("name", flat=True))

        return JsonResponse({
            "id": self.object.id,
            "text": self.object.text,
            "slug": self.object.slug,
            "status": self.object.status,
            "created": self.object.create,
            "user": self.object.user_id,
            "skills": list(self.object.skills.all().values_list("name", flat=True))
        })


@method_decorator(csrf_exempt, name="dispatch")
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
