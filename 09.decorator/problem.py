"""
Based on the sources, the problem that necessitates the Decorator pattern is the **"combinatorial explosion of subclasses"** caused by using **inheritance** to add features.

The code below implements the notification library using this problematic inheritance approach. In this scenario, you must define a new class for every possible combination of notification channels (e.g., Email+SMS, Email+Slack, Email+SMS+Slack), which creates "static" behavior that cannot be altered at runtime.
"""


### Python Code: The "Inheritance" Approach (Problematic State)
# 1. THE BASE CLASS
# "The initial version of the library was based on the Notifier class...
# [used] to send notifications about important events to a predefined set of emails."
class Notifier:
    def __init__(self, email):
        self.email = email

    def send(self, message: str):
        print(f"EMAIL sent to {self.email}: {message}")


# 2. SINGLE EXTENSIONS
# "Each notification type is implemented as a notifier's subclass."
class SMSNotifier(Notifier):
    def __init__(self, email, phone):
        super().__init__(email)
        self.phone = phone

    def send(self, message: str):
        # Calls the parent (Email) first
        super().send(message)
        # Adds SMS behavior
        print(f"SMS sent to {self.phone}: {message}")


class SlackNotifier(Notifier):
    def __init__(self, email, slack_id):
        super().__init__(email)
        self.slack_id = slack_id

    def send(self, message: str):
        # Calls the parent (Email) first
        super().send(message)
        # Adds Slack behavior
        print(f"SLACK sent to {self.slack_id}: {message}")


# 3. THE COMBINATORIAL EXPLOSION
# "You tried to address that problem by creating special subclasses which combined
# several notification methods within one class."
# "Subclasses can have just one parent class... inheritance doesn't let a class
# inherit behaviors of multiple classes at the same time."


class SMSAndSlackNotifier(Notifier):
    def __init__(self, email, phone, slack_id):
        super().__init__(email)
        self.phone = phone
        self.slack_id = slack_id

    def send(self, message: str):
        super().send(message)  # Email
        print(f"SMS sent to {self.phone}: {message}")
        print(f"SLACK sent to {self.slack_id}: {message}")


class FacebookAndSMSNotifier(Notifier):
    def __init__(self, email, fb_id, phone):
        super().__init__(email)
        self.fb_id = fb_id
        self.phone = phone

    def send(self, message: str):
        super().send(message)  # Email
        print(f"FACEBOOK post to {self.fb_id}: {message}")
        print(f"SMS sent to {self.phone}: {message}")


# 4. CLIENT CODE
if __name__ == "__main__":
    print("--- Scenario: Simple User ---")
    # "The client was supposed to instantiate the desired notification class
    # and use it for all further notifications."
    simple_user = Notifier("user@example.com")
    simple_user.send("Hello World")

    print("\n--- Scenario: Critical Alert (Static Combination) ---")
    # To get multiple channels, we are forced to instantiate a specific "Combo" class.
    # We cannot dynamically add SMS to an existing Slack object.
    critical_notifier = SMSAndSlackNotifier("admin@example.com", "555-0199", "#alerts")
    critical_notifier.send("Server is down!")


### Why this is the "Problem"
"""
1.  **Static Inheritance:** As noted in the sources, "Inheritance is static. You can’t alter the behavior of an existing object at runtime. You can only replace the whole object with another one". If a user wants to turn off SMS notifications but keep Slack, you must destroy the `SMSAndSlackNotifier` object and create a new `SlackNotifier` object.
2.  **Code Bloat:** If you add a new channel (e.g., Discord), you must create new subclasses for every possible combination (Discord+SMS, Discord+Slack, Discord+Email, etc.). This leads to the "combinatorial explosion of subclasses" mentioned in the text.
3.  **Rigid Structure:** Because subclasses generally have "just one parent class," you cannot easily inherit the logic of `SMSNotifier` and `SlackNotifier` simultaneously; you are forced to rewrite the combined logic in a new class like `SMSAndSlackNotifier`.
"""
