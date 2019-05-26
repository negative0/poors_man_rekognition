import av, abc
from progress.bar import Bar
from ..pipeline_element import PipelineElement
import numpy as np

class Person:
	def __init__(self, predicted_name, prediction_prob):
		self._predicted_name = predicted_name
		self._prediction_prob = prediction_prob

	@property
	def predicted_name(self):
		return self._predicted_name

	def get_JSON(self):
		person = {}

		person["name"] = self._predicted_name
		person["confidence"] = self._prediction_prob

		return person

class Face:
	@property
	def face_image(self):
		return self._face_image
	
	@property
	def bounding_box(self):
		return self._bounding_box

	@property
	def person(self):
		return self._person
	
	def set_person(self, predicted_name, prediction_prob):
		self._person = Person(predicted_name, prediction_prob)

	def __init__(self, face_image, bounding_box):
		self._person = None
		self._face_image = face_image
		self._bounding_box = bounding_box

	def get_JSON(self):
		face = {}

		bb = self._bounding_box
		face["bounding_box"] = {"left": float(bb[0]), "right": float(bb[1]), "top": float(bb[2]), "bottom": float(bb[3])}

		face["person"] = None
		if self._person:
			face["person"] = self._person.get_JSON()

		return face


# can be either image or video frame
class Data:
	def __init__(self, image_data):
		self._image_data = image_data
		self._faces = []

	def add_face(self, face_image, bounding_box):
		face = Face(face_image, bounding_box)
		self._faces.append(face)

	@property
	def faces(self):
		return self._faces

	@property
	def image_data(self, delete_data = False):
		if type(self._image_data) == np.ndarray:
			image_data = self._image_data

			if delete_data:
				self._image_data = None

			return image_data
		return None
	
	def get_JSON(self):
		data = {}

		faces = []

		for face in self._faces:
			f = dict()

			f["face"] = face.get_JSON()

			# f["bounding_box"]
			faces.append(f)

		data["faces"] = faces
		return data


class DataHandlerElem(PipelineElement):
	_max_frames = None
	_current_frame = 0

	def __init__(self, input_path, max_frames = None):
		self._num_of_images = 0
		self._current_frame = 0 #counter
		self._max_frames = max_frames
		self.input_path = input_path

	@property
	def max_frames(self):
		return self._max_frames

	@max_frames.setter
	def max_frames(self, max_frames):
		self._max_frames = max_frames

	@property
	def num_of_images(self):
		return self._num_of_images

	@property
	def input_path(self):
		return self._input_path

	@input_path.setter
	def input_path(self, input_path):
		self._input_path = input_path

	@num_of_images.setter
	def num_of_images(self, num_of_images):
		self._num_of_images = num_of_images

		if self._max_frames == None:
			self._max_frames = self._num_of_images