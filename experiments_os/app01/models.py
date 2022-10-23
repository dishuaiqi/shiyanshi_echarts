from django.db import models

# Create your models here.

class Pcr(models.Model):
    date=models.DateField(verbose_name='日期')
    partment=models.CharField(verbose_name='公司',max_length=32)
    bumen=models.CharField(verbose_name='部门',max_length=32)
    sampleType=models.CharField(verbose_name='样本类型',max_length=32)
    viruestype=models.CharField(verbose_name='检测类型',max_length=32)
    testkit=models.CharField(verbose_name='试剂盒',max_length=32)
    sampleInformation=models.CharField(verbose_name='样本信息',max_length=128)
    reschoices=(
        (1,'-'),
        (2,'+'),
        (3,'可疑'),
    )
    expermentsResult=models.SmallIntegerField(verbose_name='检测结果',choices=reschoices,default=1)
    FAM=models.CharField(verbose_name='fam值',max_length=32)
    price=models.IntegerField(verbose_name='单价')


class BingYuan(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    日期 = models.DateTimeField(blank=True, null=True)
    公司 = models.CharField(max_length=255, blank=True, null=True)
    部门 = models.CharField(max_length=255, blank=True, null=True)
    检测类型 = models.CharField(max_length=255, blank=True, null=True)
    试剂盒 = models.CharField(max_length=255, blank=True, null=True)
    样本类型 = models.CharField(max_length=255, blank=True, null=True)
    检测样本信息 = models.CharField(max_length=255, blank=True, null=True)
    结果 = models.CharField(max_length=255, blank=True, null=True)
    fam值 = models.CharField(db_column='FAM值', max_length=255, blank=True, null=True)  # Field name made lowercase.
    三重腹泻传染性胃肠炎 = models.CharField(max_length=255, blank=True, null=True)
    三重腹泻传染性胃肠炎值 = models.CharField(max_length=255, blank=True, null=True)
    三重腹泻轮状 = models.CharField(max_length=255, blank=True, null=True)
    三重腹泻轮状值 = models.CharField(max_length=255, blank=True, null=True)
    # price=models.IntegerField(verbose_name='单价')

    class Meta:
        managed = False
        db_table = '病原'
class kangti(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    日期 = models.DateTimeField(blank=True, null=True)
    公司 = models.TextField(db_collation='utf8_croatian_ci', blank=True, null=True)
    部门 = models.TextField(blank=True, null=True)
    猪耳号 = models.TextField(blank=True, null=True)
    猪群来源 = models.TextField(blank=True, null=True)
    猪群种类 = models.TextField(blank=True, null=True)
    原始序号 = models.TextField(blank=True, null=True)
    测样序号 = models.FloatField(blank=True, null=True)
    od值 = models.FloatField(db_column='OD值', blank=True, null=True)  # Field name made lowercase.
    计算值 = models.FloatField(blank=True, null=True)
    结果判定 = models.TextField(blank=True, null=True)
    检测类型 = models.TextField(blank=True, null=True)
    试剂盒 = models.TextField(blank=True, null=True)
    免疫记录 = models.TextField(blank=True, null=True)
    免疫剂量 = models.TextField(blank=True, null=True)
    疫苗厂家 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '抗体'