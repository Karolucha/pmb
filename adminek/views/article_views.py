from adminek.views.generic_views import BaseGenericView


class ArticleView(BaseGenericView):
    def get_for_list(self):
        return self.model_class.objects.all().order_by('date')