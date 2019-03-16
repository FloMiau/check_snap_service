# check_snap_service.py

This Nagios/Icinga plugin can be used to check Snap services. Snap services can be installed by [Snappy](https://snapcraft.io/).


## Getting Started

check_snap_service.py is a python script that checks Snap services. Python 3 has to be installed on the system.

For installation place the python file in your plugin directory `/usr/lib/nagios/plugins/`.

The plugin uses the output of `snap services $servicename` to get the state of a Snap service. The state is derived from the value of the "Current" column. The vaulue should be "active". Everything else is seen as a failure state. Please note that the "Startup" column will be ignored in this check plugin.

This Read Me uses the [Nextcloud Snap](https://github.com/nextcloud/nextcloud-snap) package as example:

    snap services nextcloud
    Service                   Startup  Current
    nextcloud.apache          enabled  active
    nextcloud.mdns-publisher  enabled  active
    nextcloud.mysql           enabled  active
    nextcloud.nextcloud-cron  enabled  active
    nextcloud.php-fpm         enabled  active
    nextcloud.redis-server    enabled  active
    nextcloud.renew-certs     enabled  active



## Usage

    usage: check_snap_service.py [-h] --service SERVICE [--ignore IGNORE]

    Icinga plugin to check snap services

    optional arguments:
    -h, --help         show this help message and exit
    --service SERVICE  Check this service(s)
	--ignore IGNORE    Optional: Ignore this service(s), separated by comma



## Examples

The following states can occur:

| State    | Situation                            |
| -------- | ------------------------------------ |
| OK       | all services are active              |
| WARNING  | never                                |
| CRITICAL | one or more services are inactive    |
| UNKNOWN  | other (e. g. services doesn't exist) |


### Everything is ok

Checks can be performed on one service only:

    ./check_snap_service.py --service nextcloud.php-fpm
    OK - service nextcloud.php-fpm is active
	
    Service            Startup  Current
    nextcloud.php-fpm  enabled  active


Checks can pe performed on a group of services:

    ./check_snap_service.py --service nextcloud
    OK - service nextcloud is active
	
    Service                   Startup  Current
    nextcloud.apache          enabled  active
    nextcloud.mdns-publisher  enabled  active
    nextcloud.mysql           enabled  active
    nextcloud.nextcloud-cron  enabled  active
    nextcloud.php-fpm         enabled  active
    nextcloud.redis-server    enabled  active
    nextcloud.renew-certs     enabled  active


One service can be ignored:

	./check_snap_service.py --service nextcloud --ignore nextcloud.nextcloud-fixer
	OK - service nextcloud is active
	
	Service                    Startup  Current   Notes
	nextcloud.apache           enabled  active    -
	nextcloud.mdns-publisher   enabled  active    -
	nextcloud.mysql            enabled  active    -
	nextcloud.nextcloud-cron   enabled  active    -
	nextcloud.nextcloud-fixer  enabled  inactive  -
	nextcloud.php-fpm          enabled  active    -
	nextcloud.redis-server     enabled  active    -
	nextcloud.renew-certs      enabled  active    -



Multiple services can be ignored:

	./check_snap_service.py --service nextcloud --ignore nextcloud.nextcloud-fixer,nextcloud.renew-certs
	OK - service nextcloud is active
	
	Service                    Startup  Current   Notes
	nextcloud.apache           enabled  active    -
	nextcloud.mdns-publisher   enabled  active    -
	nextcloud.mysql            enabled  active    -
	nextcloud.nextcloud-cron   enabled  active    -
	nextcloud.nextcloud-fixer  enabled  inactive  -
	nextcloud.php-fpm          enabled  active    -
	nextcloud.redis-server     enabled  active    -
	nextcloud.renew-certs      enabled  inactive    -


### Something is wrong

Service doesn't exist:

    ./check_snap_service.py --service foobar
    UNKNOWN - error while executing
	
    error: snap "foobar" not found


One Snap service is inactive:

    ./check_snap_service.py --service nextcloud
    CRITICAL - service nextcloud.apache is not active
	
    Service                   Startup  Current
    nextcloud.apache          enabled  inactive
    nextcloud.mdns-publisher  enabled  active
    nextcloud.mysql           enabled  active
    nextcloud.nextcloud-cron  enabled  active
    nextcloud.php-fpm         enabled  active
    nextcloud.redis-server    enabled  active
    nextcloud.renew-certs     enabled  active


Two Snap services are inactive:

    ./check_snap_service.py --service nextcloud
    CRITICAL - multiple services are not active
	
    Service                   Startup  Current
    nextcloud.apache          enabled  inactive
    nextcloud.mdns-publisher  enabled  active
    nextcloud.mysql           enabled  active
    nextcloud.nextcloud-cron  enabled  active
    nextcloud.php-fpm         enabled  active
    nextcloud.redis-server    enabled  active
    nextcloud.renew-certs     enabled  inactive


## Implemenation

In this part you can find configuration examples for Icinga 2.

### Command definiton

    object CheckCommand "check_snap_service" {
        command = [ PluginDir + "/check_snap_service.py" ] 

        arguments = {
            "--service" = {
            value = "$service$"
            required = true
            }
			"--ignore" = {
			  value = "$ignoring$"
			}
        }
    }

### Service definition

    apply Service for (unit => config in host.vars.snapservice) {
        import "generic-service"

        check_command = "check_snap_service"

        vars += config
    }

### Host definition

All nextcloud services in one check:

    object Host "nextcloud.example.org" {
        import "generic-host"


        vars.snapservice["snap nextcloud"] = {
            service = "nextcloud"
			ignoring = "nextcloud.nextcloud-fixer"
        }
    }

One check per necxtcloud service:

    object Host "nextcloud.example.org" {
        import "generic-host"

        vars.snapservice["snap nextcloud.apache"] = {
            service = "nextcloud.apache"
        }
        vars.snapservice["snap nextcloud.mysql"] = {
            service = "nextcloud.mysql"
        }
        vars.snapservice["snap nextcloud.php-fpm"] = {
            service = "nextcloud.php-fpm"
        }
        vars.snapservice["snap nextcloud.redis-server"] = {
            service = "nextcloud.redis-server"
        }
        vars.snapservice["snap nextcloud.renew-certs"] = {
            service = "nextcloud.renew-certs"
        }
        vars.snapservice["snap nextcloud.mdns-publisher"] = {
            service = "nextcloud.mdns-publisher"
        }
        vars.snapservice["snap nextcloud.nextcloud-cron"] = {
            service = "nextcloud.nextcloud-cron"
        }
    }


## Author

Florian Köttner, 2018


## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

