from django.contrib import admin
from .models import Property, Feature
from django.contrib.auth.models import User

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id','title', 'location', 'starting_price', 'category', 'num_beds', 'num_bathrooms', 'agent')
    search_fields = ('title', 'location', 'category', 'agent__username')
    list_filter = ('category',)  # Keep only category here; we'll handle agents differently below.

    def get_queryset(self, request):
        # Ensure that only properties associated with agents (is_staff=True) are shown
        queryset = super().get_queryset(request)
        return queryset.filter(agent__is_staff=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "agent":
            # Limit the dropdown to users with is_staff=True
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def agent_filter(self, request):
        # Show only agents in the filter
        return User.objects.filter(is_staff=True)

    # Add a custom filter for agents
    class AgentListFilter(admin.SimpleListFilter):
        title = 'Agent'  # Displayed name in the filter section
        parameter_name = 'agent'  # The query parameter for the filter

        def lookups(self, request, model_admin):
            # Return a list of agents for the filter dropdown
            agents = User.objects.filter(is_staff=True)
            return [(agent.id, agent.username) for agent in agents]

        def queryset(self, request, queryset):
            # Filter the queryset based on the selected agent
            if self.value():
                return queryset.filter(agent_id=self.value())
            return queryset

    # Add the agent filter to the list_filter
    list_filter = ('category', AgentListFilter)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the models with the custom admin configurations
admin.site.register(Property, PropertyAdmin)
admin.site.register(Feature, FeatureAdmin)
