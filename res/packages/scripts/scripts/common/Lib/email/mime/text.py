# 2017.08.29 21:56:24 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/common/Lib/email/mime/text.py
"""Class representing text/* type MIME documents."""
__all__ = ['MIMEText']
from email.encoders import encode_7or8bit
from email.mime.nonmultipart import MIMENonMultipart

class MIMEText(MIMENonMultipart):
    """Class for generating text/* type MIME documents."""

    def __init__(self, _text, _subtype = 'plain', _charset = 'us-ascii'):
        """Create a text/* type MIME document.
        
        _text is the string for this message object.
        
        _subtype is the MIME sub content type, defaulting to "plain".
        
        _charset is the character set parameter added to the Content-Type
        header.  This defaults to "us-ascii".  Note that as a side-effect, the
        Content-Transfer-Encoding header will also be set.
        """
        MIMENonMultipart.__init__(self, 'text', _subtype, **{'charset': _charset})
        self.set_payload(_text, _charset)
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\common\Lib\email\mime\text.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:56:25 St�edn� Evropa (letn� �as)
