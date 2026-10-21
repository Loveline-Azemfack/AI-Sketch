
import cv2
import numpy as np
import pytest

from src.image_processing import (
    IMAGE_SIZE,
    load_image,
    is_blank_image,
    preprocess_image,
)


def test_load_image_from_numpy():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    result = load_image(image)

    assert np.array_equal(result, image)
    assert result is not image


def test_load_image_from_file(tmp_path):
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image_path = tmp_path / "test.png"
    cv2.imwrite(str(image_path), image)

    result = load_image(str(image_path))

    assert result.shape == (100, 100, 3)


def test_load_image_file_not_found():
    with pytest.raises(ValueError):
        load_image("image_inexistante.png")


def test_load_image_empty_array():
    image = np.array([], dtype=np.uint8)

    with pytest.raises(ValueError):
        load_image(image)


def test_load_image_invalid_source():
    with pytest.raises(TypeError):
        load_image(123)


def test_is_blank_image():
    image = np.full((100, 100), 255, dtype=np.uint8)

    assert is_blank_image(image) is True


def test_is_not_blank_image():
    image = np.full((100, 100), 255, dtype=np.uint8)
    cv2.line(image, (10, 10), (90, 90), 0, 3)

    assert is_blank_image(image) is False


def test_preprocess_image_shape():
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    result = preprocess_image(image)

    assert result.shape == (28, 28, 1)
    assert result.shape[:2] == IMAGE_SIZE[::-1]


def test_preprocess_image_normalization():
    image = np.full((100, 100), 128, dtype=np.uint8)

    result = preprocess_image(image)

    assert result.dtype == np.float32
    assert np.all(result >= 0.0)
    assert np.all(result <= 1.0)
    assert np.allclose(result, 128 / 255.0)


def test_preprocess_image_invalid_dimensions():
    image = np.zeros((10, 10, 3, 1), dtype=np.uint8)

    with pytest.raises(ValueError):
        preprocess_image(image)
