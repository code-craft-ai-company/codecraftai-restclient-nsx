"""
    .. module:: securityspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Request specs for NSX-T security groups and distributed
        firewall rules / policies.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Dict, List, Optional


class SecurityGroupSpec:
    """
        Typed request spec for the security group ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        expression: Optional[List[Dict[str, object]]] = None,
    ) -> None:
        """
            Initialise a :class:`SecurityGroupSpec`.

            :param display_name: Human-readable name for the group.
            :param expression: Group membership expression entries.

            :returns: ``None``
        """
        self._display_name = display_name
        self._expression = expression
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {"display_name": self._display_name}
        if self._expression is not None:
            rtnval["expression"] = list(self._expression)
        return rtnval


class DfwRuleSpec:
    """
        Typed request spec for a distributed-firewall rule ``PATCH``
        body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        action: str = "ALLOW",
        source_groups: Optional[List[str]] = None,
        destination_groups: Optional[List[str]] = None,
        services: Optional[List[str]] = None,
        direction: str = "IN_OUT",
        sequence_number: Optional[int] = None,
    ) -> None:
        """
            Initialise a :class:`DfwRuleSpec`.

            :param display_name: Human-readable name for the rule.
            :param action: Rule action (``ALLOW`` / ``DROP`` /
                ``REJECT``).
            :param source_groups: Source group paths (or ``ANY``).
            :param destination_groups: Destination group paths.
            :param services: Service paths the rule applies to.
            :param direction: Traffic direction.
            :param sequence_number: Ordering sequence number.

            :returns: ``None``
        """
        self._display_name = display_name
        self._action = action
        self._source_groups = source_groups
        self._destination_groups = destination_groups
        self._services = services
        self._direction = direction
        self._sequence_number = sequence_number
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "action": self._action,
            "direction": self._direction,
        }
        if self._source_groups is not None:
            rtnval["source_groups"] = list(self._source_groups)
        if self._destination_groups is not None:
            rtnval["destination_groups"] = list(self._destination_groups)
        if self._services is not None:
            rtnval["services"] = list(self._services)
        if self._sequence_number is not None:
            rtnval["sequence_number"] = self._sequence_number
        return rtnval


class DfwPolicySpec:
    """
        Typed request spec for a distributed-firewall security policy
        ``PATCH`` body.
    """

    def __init__(
        self,
        *,
        display_name: str,
        category: str = "Application",
        rules: Optional[List[Dict[str, object]]] = None,
    ) -> None:
        """
            Initialise a :class:`DfwPolicySpec`.

            :param display_name: Human-readable name for the policy.
            :param category: Policy category (e.g. ``Application``).
            :param rules: Inline rule body dictionaries.

            :returns: ``None``
        """
        self._display_name = display_name
        self._category = category
        self._rules = rules
        return

    def to_dict(self) -> Dict[str, object]:
        """
            Render the spec as the NSX-T policy request body.

            :returns: The request body dictionary.
        """
        rtnval: Dict[str, object] = {
            "display_name": self._display_name,
            "category": self._category,
        }
        if self._rules is not None:
            rtnval["rules"] = list(self._rules)
        return rtnval
