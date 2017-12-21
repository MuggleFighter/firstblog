# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):
    comment_content = forms.CharField(max_length=150, min_length=10,  # 自带限制验证
                                      error_messages={'max_length': '最多150字哦',
                                                      # 'min_length': '最少10字哦!',
                                                      'required': '客官,不填内容就提交是犯规的!'
                                                      },
                                      widget=forms.Textarea(attrs={'rows': 3}),
                                      label='评论内容')
