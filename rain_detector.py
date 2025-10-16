

#  N5346 ---- ILMENAU               50.41   10.54   498

from wetterdienst import Resolution, Period

from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType

stations = DwdMosmixRequest(parameter="large", mosmix_type=DwdMosmixType.LARGE).filter_by_station_id(

    station_id=["01001", "01008"]

)



print(stations.values.all().df.head())