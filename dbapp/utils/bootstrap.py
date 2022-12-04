from django import forms
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            #字段中有属性
            if field.widget.attrs:
              field.widget.attrs["class"]="form-control"
              field.widget.attrs["placeholder"]=field.label
            else:
              field.widget.attrs = {
                  "class": "form-control",
                  "placeholder": field.label
                  }
