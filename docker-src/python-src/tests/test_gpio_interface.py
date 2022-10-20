import pytest
import sys
sys.path.append("..")

from gpio_interface import gpio_device,Pin
import cattrs

def test_creating():
	a = gpio_device(given_instance_name="blahblahblahblahblah")
	assert a.friendly_name == "Uknown GPIO Device"
	assert a.given_instance_name == "blahblahblahblahblah"
	assert a.in_group == ""
	assert a.Pin_NEG is None
	assert a.Pin_POS is None
	assert a.validate_pins() == False
	with pytest.raises(ValueError):
		a.given_instance_name = "This name will be too long"
		a.in_group = "This name will be too long"

def test_pins():
	a = gpio_device(given_instance_name="blah?",in_group="Grop",Pin_NEG="A0",Pin_POS="B0")
	assert isinstance(a.Pin_NEG,Pin)
	assert a.Pin_POS == "B0"
	assert a.validate_pins() == False
	a.Pin_POS = "A0"
	assert a.validate_pins()
	
def test_serializing():
	a = gpio_device(given_instance_name="blah?",in_group="Grop",Pin_NEG="A0")
	b = cattrs.unstructure(a)
	assert b["friendly_name"] == "Uknown GPIO Device"
	assert b["given_instance_name"] == "blah?"
	assert b["in_group"] == "Grop"
	assert isinstance(b["Pin_NEG"],Pin)
	assert b["Pin_POS"] is None

def test_deserializing():
	a = gpio_device(given_instance_name="blah?",in_group="Grop",Pin_NEG="A0")
	b = cattrs.unstructure(a)
	c = cattrs.structure(b,gpio_device)
	assert c.friendly_name == "Uknown GPIO Device"
	assert c.given_instance_name == "blah?"
	assert c.in_group == "Grop"
	assert isinstance(c.Pin_NEG,Pin)
	assert c.Pin_POS is None
	assert a.validate_pins() == False