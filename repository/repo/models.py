from django.db import models

# Create your models here.


class NovelAuthor(models.Model):
    name = models.CharField(max_length=32, verbose_name="作者名称", unique=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "tb_novel_author"

    def __str__(self):
        return self.name


class NovelCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name="小说分类", unique=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "tb_novel_category"

    def __str__(self):
        return self.name


class Novel(models.Model):
    url_id = models.CharField(max_length=64, verbose_name="url唯一标识", primary_key=True)
    url = models.CharField(max_length=255, verbose_name="小说链接", unique=True)
    image_url = models.CharField(max_length=255, verbose_name="小说图片", null=True, blank=True)
    image_path = models.CharField(max_length=255, verbose_name="小说图片路径", null=True, blank=True)
    site_name = models.CharField(max_length=32, verbose_name="网站名称")
    novel_name = models.CharField(max_length=64, verbose_name="小说名称", unique=True)
    author = models.ForeignKey(NovelAuthor, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(NovelCategory, on_delete=models.CASCADE, verbose_name="分类")
    intro = models.TextField(verbose_name="简介", null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "tb_novel"

    def __str__(self):
        return self.novel_name


class Chapter(models.Model):
    url_id = models.CharField(max_length=64, verbose_name="url唯一标识", primary_key=True)
    url = models.CharField(max_length=255, verbose_name="章节链接", unique=True)
    index = models.PositiveIntegerField(verbose_name="章节顺序", unique=True)
    name = models.CharField(max_length=128, verbose_name="章节名称")
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name="所属小说")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "tb_chapter"

    def __str__(self):
        return self.name
