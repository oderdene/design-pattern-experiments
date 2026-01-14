"""
Based on the "Decorator" design pattern described in your sources, here is a Python implementation for a notification library.

This code addresses the problem where a library needs to support multiple notification types (Email, SMS, Slack, Facebook) without creating a "combinatorial explosion of subclasses". Instead of inheritance, it uses **composition** to wrap objects in "decorators" that add new behaviors dynamically,.
"""

### Python Code: Notification Library (Decorator Pattern)


from abc import ABC, abstractmethod


# 1. THE COMPONENT INTERFACE
# "The Component declares the common interface for both wrappers and wrapped objects."
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


# 2. CONCRETE COMPONENT
# "The simple email notification behavior inside the base Notifier class."
# "Concrete Component is a class of objects being wrapped. It defines the basic behavior."
class EmailNotifier(Notifier):
    def __init__(self, email_address):
        self.email_address = email_address

    def send(self, message: str):
        print(f"EMAIL sent to {self.email_address}: {message}")


# 3. BASE DECORATOR
# "The Base Decorator class has a field for referencing a wrapped object."
# "The wrapper contains the same set of methods as the target and delegates to it all requests."
class BaseNotificationDecorator(Notifier):
    def __init__(self, wrappee: Notifier):
        self._wrappee = wrappee  # The "wrappee" field

    def send(self, message: str):
        # Delegate work to the wrapped component
        self._wrappee.send(message)


# 4. CONCRETE DECORATORS
# "Concrete Decorators define extra behaviors that can be added to components dynamically."
# "Each notification type is implemented as a notifier's subclass." (But as decorators now)


class SMSDecorator(BaseNotificationDecorator):
    def __init__(self, wrappee: Notifier, phone_number):
        super().__init__(wrappee)
        self.phone_number = phone_number

    def send(self, message: str):
        # 1. Execute new behavior (SMS)
        print(f"SMS sent to {self.phone_number}: {message}")
        # 2. Delegate to the parent/wrapped object
        super().send(message)


class FacebookDecorator(BaseNotificationDecorator):
    def __init__(self, wrappee: Notifier, fb_id):
        super().__init__(wrappee)
        self.fb_id = fb_id

    def send(self, message: str):
        # 1. Execute new behavior (Facebook)
        print(f"FACEBOOK post to ID {self.fb_id}: {message}")
        # 2. Delegate to the parent/wrapped object
        super().send(message)


class SlackDecorator(BaseNotificationDecorator):
    def __init__(self, wrappee: Notifier, slack_channel):
        super().__init__(wrappee)
        self.slack_channel = slack_channel

    def send(self, message: str):
        # 1. Execute new behavior (Slack)
        print(f"SLACK message to #{self.slack_channel}: {message}")
        # 2. Delegate to the parent/wrapped object
        super().send(message)


# 5. CLIENT CODE
# "The Client can wrap components in multiple layers of decorators."
if __name__ == "__main__":
    print("--- Scenario 1: Basic Email Only ---")
    # The client works with a pure notifier object
    simple_notifier = EmailNotifier("admin@example.com")
    simple_notifier.send("Server is starting.")

    print("\n--- Scenario 2: Critical Issue (Email + SMS + Slack) ---")
    # "The client would need to wrap a basic notifier object into a set of decorators."
    # "The resulting objects will be structured as a stack."

    # 1. Create base
    stack = EmailNotifier("admin@example.com")

    # 2. Wrap with SMS
    stack = SMSDecorator(stack, "+1-555-0199")

    # 3. Wrap with Slack
    stack = SlackDecorator(stack, "dev-ops-alerts")

    # "The last decorator in the stack would be the object that the client actually works with."
    # sending a message now triggers the chain behavior
    stack.send("CRITICAL: Server is on fire!")


### Explanation of the Implementation
"""
**1. The Component Interface (`Notifier`)**
This defines the `send` method. By ensuring both the basic notifier and the decorators share this interface, the client code can treat them identically, unaware of whether it is using a "pure" object or a decorated one,.

**2. The Concrete Component (`EmailNotifier`)**
The sources suggest leaving the "simple email notification behavior" in the base class. This class performs the actual basic work and ends the chain of delegation.

**3. The Base Decorator (`BaseNotificationDecorator`)**
This class holds a reference field (`_wrappee`) to another `Notifier` object,. It implements the `send` method by simply calling `send` on the wrapped object. This delegation is the core mechanism that allows decorators to be stacked.

**4. The Concrete Decorators (`SMS`, `Facebook`, `Slack`)**
These classes extend the base decorator. They override the `send` method to execute their specific behavior (e.g., sending an SMS) and then call the parent method to pass the request down the stack. This solves the "combinatorial explosion" problem because you can combine these behaviors at runtime rather than creating static subclasses like `EmailAndSMSNotifier`,.

**5. Client Usage (Stacking)**
In the "Scenario 2" example, the code demonstrates how an application can configure complex stacks of notification decorators. This mimics the real-world analogy provided in the text: wearing a sweater, then a jacket, then a raincoat on top of your basic self.
"""
