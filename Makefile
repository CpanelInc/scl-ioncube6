OBS_PROJECT := EA4
scl-php70-php-ioncube6-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php56-php-ioncube6-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php55-php-ioncube6-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
scl-php54-php-ioncube6-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
OBS_PACKAGE := scl-ioncube6
include $(EATOOLS_BUILD_DIR)obs-scl.mk
