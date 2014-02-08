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

__author__ = 'evan'

class rawSQL():

    make_increment_headers = '''CREATE TABLE {0}.basic_increments_{1} (
            wkb_geometry geometry,
            id_grid integer PRIMARY KEY,
            placetype_id integer,
            pop_inc integer,
            du_inc integer,
            emp_inc integer,
            du_detsf_ll_inc integer,
            du_attsf_inc integer,
            du_mf_inc integer,
            emp_ret_inc integer,
            emp_off_inc integer,
            emp_ind_inc integer,
            urban_ldc integer,
            compact_ldc integer,
            refill integer);
            '''

    select_and_buffer_study_area_stops = '''
                CREATE TABLE    {1}
                AS
                SELECT          distinct(b.ogc_fid),

                CASE WHEN       mode = 'HSR'
                    THEN        ST_Buffer(b.wkb_geometry, {5})
                    ELSE        ST_Buffer(b.wkb_geometry, {6})
                        END AS  wkb_geometry,

                                mode,
                                station,
                                b.date as date_open

                FROM            {0}.{2} a,
                                inputs_outputs_statewide.transit_stations b

                WHERE           (
                                date <= {3}
                            AND mode <> 'HSR'
                            AND ST_DWithin(a.wkb_geometry, b.wkb_geometry, {6})
                            AND {7} = 1
                                )
                        OR
                                (
                                date <= {3}
                            AND mode = 'HSR'
                            AND ST_DWithin(a.wkb_geometry, b.wkb_geometry, {5})
                            AND {7} = 1
                                );

                CREATE INDEX    {4}_geom
                on              {1}
                using           GIST(wkb_geometry);

                ALTER TABLE     {1}
                add PRIMARY KEY (ogc_fid);'''

    copy_table = '''CREATE TABLE {0}.{1} AS SELECT * FROM {2}.{3};
                    '''

    geom_index = '''CREATE INDEX {1}_geom_idx on {0}.{1} using GIST (wkb_geometry);
                    '''

    add_pkey = '''ALTER TABLE {0}.{1} ADD PRIMARY KEY (id_grid);'''

    import_canvas = '''create table {0}.{1} as select
                        ST_Transform(wkb_geometry, 900913) as wkb_geometry,
                        id_grid,
                        placetype_id,
                        placetype_id as initial_placetype,
                        placetype_id as last_placetype
                        from {4};

                    alter table {0}.{1}
                        add column dirty boolean,
                        add column painted boolean,
                        add column raw boolean;

                    update {0}.{1}
                        set wkb_geometry = setSRID(wkb_geometry, 900913) where SRID(wkb_geometry) <> 900913;
                    update {0}.{1} set raw = True;'''

    create_canvas = '''create table {0}.{1} as select
                        ST_Transform(wkb_geometry, 900913) as wkb_geometry,
                        id_grid
                        from {2}.{3};

                    alter table {0}.{1}
                        add column placetype_id varchar(6),
                        add column initial_placetype varchar(6),
                        add column last_placetype varchar(6),
                        add column dirty boolean,
                        add column painted boolean
                        add column raw boolean;

                    update {0}.{1}
                        set wkb_geometry = setSRID(wkb_geometry, 900913) where SRID(wkb_geometry) <> 900913;
                    update {0}.{1} set raw = True;
                    '''