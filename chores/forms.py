from django import forms

from .models import Chore, Household


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ["name"]


class JoinHouseholdForm(forms.Form):
    join_code = forms.CharField(max_length=8)


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["name", "description", "frequency", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

    def clean_frequency(self):
        frequency = self.cleaned_data["frequency"].lower()
        if frequency != "weekly":
            raise forms.ValidationError("Only weekly chores are supported in the first version.")
        return frequency
