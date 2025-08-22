import numpy as np



def ts_max(x: np.ndarray, window_size: int) -> np.ndarray:
    if window_size > x.shape[0]:
        raise ValueError("The window size cannot be greater than the number of time points")
    windows = np.lib.stride_tricks.sliding_window_view(x, window_shape=(window_size,), axis=0)
    max_value = np.nanmax(windows, axis=2)
    return max_value

def ts_min(x: np.ndarray, window_size: int) -> np.ndarray:
    if window_size > x.shape[0]:
        raise ValueError("The window size cannot be greater than the number of time points")
    windows = np.lib.stride_tricks.sliding_window_view(x, window_shape=(window_size,), axis=0)
    min_value = np.nanmin(windows, axis=2)
    return min_value

def ts_mean(x: np.ndarray, window_size: int) -> np.ndarray:
    if window_size > x.shape[0]:
        raise ValueError("The window size cannot be greater than the number of time points")
    windows = np.lib.stride_tricks.sliding_window_view(x, window_shape=(window_size,), axis=0)
    mean_value = np.nanmean(windows, axis=2)
    return mean_value

def ts_median(x: np.ndarray, window_size: int) -> np.ndarray:
    if window_size > x.shape[0]:
        raise ValueError("The window size cannot be greater than the number of time points")
    windows = np.lib.stride_tricks.sliding_window_view(x, window_shape=(window_size,), axis=0)
    median_value = np.nanmedian(windows, axis=2)
    return median_value