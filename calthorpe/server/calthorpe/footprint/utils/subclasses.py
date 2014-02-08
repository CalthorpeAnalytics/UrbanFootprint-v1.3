# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

__author__ = 'calthorpe'

def get_subclasses(classes, level=0):
    """
        Return the list of all subclasses given class (or list of classes) has.
        Inspired by this question:
        http://stackoverflow.com/questions/3862310/how-can-i-find-all-subclasses-of-a-given-class-in-python
    """
    # for convenience, only one class can can be accepted as argument
    # converting to list if this is the case
    if not isinstance(classes, list):
        classes = [classes]

    if level < len(classes):
        classes += classes[level].__subclasses__()
        return get_subclasses(classes, level+1)
    else:
        return classes

def receiver_subclasses(signal, sender, dispatch_uid_prefix, **kwargs):
    """
    A decorator for connecting receivers and all receiver's subclasses to signals. Used by passing in the
    signal and keyword arguments to connect::

        @receiver_subclasses(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs)G:
            ...
    """
    def _decorator(func):
        all_senders = get_subclasses(sender)
        for snd in all_senders:
            signal.connect(func, sender=snd, dispatch_uid=dispatch_uid_prefix+'_'+snd.__name__, **kwargs)
        return func
    return _decorator

def connect_subclasses(func, signal, sender, dispatch_uid_prefix, **kwargs):
    all_senders = get_subclasses(sender)
    for snd in all_senders:
        signal.connect(func, sender=snd, dispatch_uid=dispatch_uid_prefix+'_'+snd.__name__, **kwargs)
