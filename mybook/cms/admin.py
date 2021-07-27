from django.contrib import admin

from cms.models import Book, Impression


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'page',)
    list_display_links = ('id', 'title',)


admin.site.register(Book, BookAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
    raw_id_fields = ('book',)


admin.site.register(Impression, ImpressionAdmin)



# admin.site.register(Book)
# admin.site.register(Impression)