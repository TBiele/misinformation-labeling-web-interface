from django import forms

from .models import Misconception


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        for index, (option_value, option_label) in enumerate(self.choices):
            if option_value is None:
                option_value = ""

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (not has_selected or self.allow_multiple_selected) and str(
                    subvalue
                ) in value
                has_selected |= selected
                descriptions = [
                    misconception.description
                    for misconception in Misconception.objects.all().order_by(
                        "list_position"
                    )
                ]
                description = descriptions[index]
                subgroup.append(
                    self.create_option(
                        name,
                        subvalue,
                        sublabel,
                        selected,
                        index,
                        subindex=subindex,
                        attrs=attrs,
                        description=description,
                    )
                )
                if subindex is not None:
                    subindex += 1
        return groups

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
        description="",
    ):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        option_attrs = (
            self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        )
        if selected:
            option_attrs.update(self.checked_attribute)
        if "id" in option_attrs:
            option_attrs["id"] = self.id_for_label(option_attrs["id"], index)
            option_attrs["class"] = "hovertext"
            option_attrs["data-hover"] = description
        return {
            "name": name,
            "value": value,
            "label": label,
            "selected": selected,
            "index": index,
            "attrs": option_attrs,
            "type": self.input_type,
            "template_name": self.option_template_name,
            "wrap_label": True,
        }


class CustomMultipleChoiceField(forms.MultipleChoiceField):
    def __init__(self, *, choices=(), **kwargs):
        self.descriptions = kwargs.pop("descriptions", {})
        super().__init__(**kwargs)
        self.choices = choices


class LoginForm(forms.Form):
    user_name = forms.CharField(label="Bitte gib (d)einen Namen* ein:", max_length=100)


class LabelForm(forms.Form):
    # Populate multiple choice checkboxes with misconceptions
    misconceptions = Misconception.objects.all().order_by("list_position")
    options = [
        (misconception.id, misconception.name) for misconception in misconceptions
    ]
    descriptions = [misconception.description for misconception in misconceptions]
    selected_misconception_ids = CustomMultipleChoiceField(
        label="",
        widget=CustomCheckboxSelectMultiple,
        choices=options,
        descriptions=descriptions,
        required=False,
    )
