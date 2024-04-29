class AnalyticsRouter:
    route_app_label = 'analytics'

    def db_for_read(self, model, **hints):
        """
        Reads from the analytics database
        """
        if model._meta.app_label == self.route_app_label:
            return 'analytics'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Writes to the analytics database
        """
        if model._meta.app_label == self.route_app_label:
            return 'analytics'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the analytics app is involved
        """
        if (obj1._meta.app_label == self.route_app_label
            or obj2._meta.app_label == self.route_app_label):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        We shouldn't allow this for the analytics DB
        """
        if app_label == self.route_app_label:
            return False
        return None
