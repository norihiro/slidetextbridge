'''
Retreive text from current slideshow
'''

import re
import win32com.client
import pywintypes

# See also:
# - https://learn.microsoft.com/en-us/office/vba/api/powerpoint.slideshowwindows

class _Const:
    # pylint: disable=R0903
    ppSlideShowBlackScreen = 3
    ppSlideShowWhiteScreen = 4
    ppSlideShowDone = 5

    ppPlaceholderTitle = 1
    ppPlaceholderSubtitle = 2
    ppPlaceholderText = 3
    ppPlaceholderCenterTitle = 4
    ppPlaceholderBody = 5
    ppPlaceholderPic = 6
    ppPlaceholderObject = 7

def _convert_object(obj, std_params=(), params=()):
    d = {}
    def _f(attrname, f_conv=None):
        dest = re.sub('(.)([A-Z])', r'\1_\2', attrname).lower()
        try:
            v = getattr(obj, attrname)
        except (AttributeError, pywintypes.com_error): # pylint: disable=no-member
            return
        if f_conv:
            v = f_conv(v)
        d[dest] = v
    for attrname in std_params:
        _f(attrname)
    for attrname, f_conv in params:
        _f(attrname, f_conv)
    return d

def _com32bool_to_bool(b):
    return bool(b)

def _font_to_dict(font):
    return _convert_object(font, std_params=('Size', 'Bold', 'Name', 'BaselineOffset'), params=(
            ('Italic', _com32bool_to_bool),
            ('Subscript', _com32bool_to_bool),
            ('Superscript', _com32bool_to_bool),
    ))

def _tr_to_dict(tr):
    return _convert_object(
            tr,
            std_params=(
                'Text',
                'Count', 'Start', 'Length',
                'BoundLeft', 'BoundTop', 'BoundWidth', 'BoundHeight',
            ),
            params=(
                ('Font', _font_to_dict),
                ('HasText', _com32bool_to_bool),
            ),
    )

def _tf_to_dict(tf):
    return _convert_object(tf, std_params=('Orientation', ), params=(
            ('TextRange', _tr_to_dict),
            ('HasText', _com32bool_to_bool),
            ('WordWrap', _com32bool_to_bool),
    ))

def _pf_to_dict(pf):
    return _convert_object(pf, std_params=('Name', 'Type', 'ContainedType'))

def _shape_to_dict(shape):
    return _convert_object(shape, std_params=('Name', 'Type'), params=(
            ('TextFrame', _tf_to_dict),
            ('PlaceholderFormat', _pf_to_dict),
    ))


class NoUpdate(Exception):
    'Exception class if `check_outdated` set and the slide is same as previous.'

class _Uninitialized:
    # pylint: disable=R0903
    pass

class PPTText:
    '''
    Communicate with PowerPoint and get slideshow text
    '''

    def __init__(self):
        self.last_slide = _Uninitialized()
        self._placeholder_types = (
                _Const.ppPlaceholderTitle,
                _Const.ppPlaceholderSubtitle,
                _Const.ppPlaceholderText,
                _Const.ppPlaceholderCenterTitle,
                _Const.ppPlaceholderBody,
                _Const.ppPlaceholderObject,
        )
        self.ppt = None
        self._last_window = None

    def _connect_ppt(self):
        self.ppt = win32com.client.Dispatch("PowerPoint.Application")
        self._last_window = None

    def _current_slideshow_window(self):
        if not self.ppt:
            self._connect_ppt()
        try:
            slide_count = self.ppt.SlideShowWindows.Count
        except (pywintypes.com_error, AttributeError): # pylint: disable=no-member
            self.ppt = None
            self._last_window = None
            return None

        if slide_count == 1:
            self._last_window = self.ppt.SlideShowWindows(1)
            return self._last_window

        cand = False
        for ix in range(slide_count):
            w = self.ppt.SlideShowWindows(ix + 1)
            if w.Active:
                self._last_window = w
                return w
            if w == self._last_window:
                cand = w
        return cand

    def get_slide(self, check_outdated=False):
        '''
        Get current presentation slide

        :return:  The slide object
        '''
        w = self._current_slideshow_window()
        if not w:
            # no current presentation window
            return self._check_outdated(None, check_outdated)

        view = w.View

        if view.State in (
                _Const.ppSlideShowBlackScreen,
                _Const.ppSlideShowWhiteScreen,
                _Const.ppSlideShowDone):
            return self._check_outdated(None, check_outdated)

        slide = view.Slide

        return self._check_outdated(slide, check_outdated)

    def _check_outdated(self, slide, check_outdated):
        # We may also check `SlideElapsedTime`
        if check_outdated:
            if self.last_slide == slide:
                raise NoUpdate()
        self.last_slide = slide
        return slide

    def slide_texts(self, slide):
        '''
        Convert Slide object to list of strings
        '''

        texts = []
        for shape in slide.Shapes:
            if not shape.HasTextFrame or not shape.TextFrame.HasText:
                continue

            if not self._filter_shape(shape):
                continue

            text = shape.TextFrame.TextRange.Text.replace('\r', ' ')
            texts.append(text)

        return texts

    def slide_text(self, slide):
        '''
        Convert Slide object to string
        '''
        return '\n'.join(self.slide_texts(slide))

    def _filter_shape(self, shape):
        if shape.Type == 14: # a placeholder
            if shape.PlaceholderFormat.Type in self._placeholder_types:
                return True
        return False

    def slide_dicts(self, slide):
        '''
        Convert shapes in the slide to a list of dict objects.
        '''

        shapes = []
        for shape in slide.Shapes:
            shapes.append(_shape_to_dict(shape))
        return {'shapes': shapes}


def _join_any(obj, delimiter='\n'):
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return None
    if isinstance(obj, dict):
        for key in ('text', 'text_range', 'text_frame'):
            if key in obj:
                return _join_any(obj[key], delimiter=delimiter)
        return None
    return delimiter.join([_join_any(x, delimiter=delimiter) for x in obj if x])


def example_loop():
    'Example implementation to poll the slide'
    # pylint: disable=C0415
    import argparse
    import json
    import time

    parser = argparse.ArgumentParser()
    # Examples:
    #   --jmespath-filter 'shapes[?placeholder_format.type==`7`].text_frame'
    #   --jmespath-filter 'shapes[?text_frame.text_range.font.size>=`28`].text_frame'
    parser.add_argument('--jmespath-filter', action='store', default=None)
    parser.add_argument('--print-raw', action='store_true', default=False)
    args = parser.parse_args()

    if args.jmespath_filter:
        import jmespath
        jmespath_filter = jmespath.compile(args.jmespath_filter)
    else:
        jmespath_filter = None

    try:
        p = PPTText()

        while True:
            try:
                slide = p.get_slide(check_outdated=True)
            except NoUpdate:
                time.sleep(1)
                continue

            if not slide:
                print('Empty\n')
                time.sleep(1)
                continue

            obj = p.slide_dicts(slide)
            if args.print_raw:
                print(json.dumps(obj, ensure_ascii=False, indent=2))

            if jmespath_filter:
                obj = jmespath_filter.search(obj)
                text = _join_any(obj).replace('\r', ' ').strip()
            else:
                text = p.slide_text(slide).replace('\r', ' ').strip()

            if jmespath_filter or not args.print_raw:
                print(text)

            print('')
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    example_loop()
