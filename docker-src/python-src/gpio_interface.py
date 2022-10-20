from attrs import define, field, validators, Factory
import cattrs
try:
	from microcontroller import Pin
	import board
except NotImplementedError:
	class Pin:
			blah = "blah"
	class board:
		A0 = Pin()

VALID_PINS = dir(board)

def deserialize_str_to_pin(pin_name: str) -> Pin:
	"""Attempts to convert a pin name from string to a CircuitPython Pin object"""
	if pin_name is None:
		return None
	try:
		pin_index = VALID_PINS.index(pin_name)
		return getattr(board,VALID_PINS[pin_index])
	except ValueError:
		return pin_name

@define(kw_only=True)
class gpio_device:
	friendly_name: str = field(default="Uknown GPIO Device")
	given_instance_name: str = field(default="",validator=[validators.max_len(20)])
	in_group: str = field(default="",validator=[validators.max_len(20)])
	Pin_POS: Pin = field(default=None,converter=deserialize_str_to_pin,validator=[validators.optional(validators.instance_of((Pin,str)))])
	Pin_NEG: Pin = field(default=None,converter=deserialize_str_to_pin,validator=[validators.optional(validators.instance_of((Pin,str)))])

	def validate_pins(self):
		"""Returns true if all required pins to run the GPIO device exist on the board, as reported by CircuitPython"""
		return all([isinstance(pin,Pin) for pin in [self.Pin_NEG, self.Pin_POS]])

@define(kw_only=True)
class h_bridge(gpio_device):
	Pin7_POS_logic: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])
	Pin8_NEG_logic: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])
	Pin1_Fwd_PWM: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])
	Pin2_Bwd_PWM: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])
	Pin3_Fwd_Enable: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])
	Pin4_Bwd_Enable: Pin = field(default=None,validator=[validators.optional(validators.instance_of((str)))])

	def validate_pins(self):
		"""Returns true if all required pins to run the GPIO device exist on the board, as reported by CircuitPython"""
		return all([isinstance(pin,str) for pin in [self.Pin_NEG, self.Pin_POS]]) and super().validate_pins()


# TODO: Convert to graph ds