!-------------------------------------------------------------------------------!
!  the subroutine read_input contained in this module reads in all of the       !
!  parameters specified in the input files as well as calling a couple of       !
!  basic checks.                                                                !
!                                                                               !
!  more checks should be included here in the future.                           !
!-------------------------------------------------------------------------------!

module input

    use globals
    use class_line
    use class_geometry
    use class_dust
    use class_grid
    use class_freq_grid
    use class_obs_data

    implicit none

contains

    subroutine read_input()

     
	input_file='input/input.in'

        !read in input file and store
        open(10,file=input_file)

        !general options
        read(10,*)
        read(10,*) lg_store_all
        read(10,*) lg_data
        read(10,*) data_file
        read(10,*) data_exclusions_file
        read(10,*) lg_doublet
        read(10,*) lg_vel_shift
        read(10,*) lg_los
        read(10,*) lg_multi_los
        read(10,*) lg_es
        read(10,*) e_scat_file
        read(10,*) day_no
        read(10,*) dust%scat_type

        !geometry options
        read(10,*)
        read(10,*) lg_decoupled
        read(10,*) dust_geometry%type
        read(10,*) dust_file
        read(10,*) species_file
        read(10,*) grid_file
        read(10,*) gas_geometry%type
        read(10,*) gas_file

        read(10,*)
        read(10,*) mothergrid%n_cells(1)
        read(10,*) n_angle_divs
        read(10,*)
        read(10,*) n_packets
        read(10,*) nu_grid%n_bins
        read(10,*) num_threads
        
        read(10,*)
        read(10,*) lg_vel_law
        read(10,*) vel_max
        read(10,*) vel_min
        read(10,*) vel_power
        read(10,*)
	read(10,*) lg_xybin
        close(10)

        !check for conflict in specified dust and gas distributions
        if (.not. lg_decoupled) then
            if (gas_geometry%type /= dust_geometry%type) then
                print*, 'you have requested that dust and gas should be coupled but specified different geometry types. aborted'
                stop
            end if
        end if

        !read in gas options
        open(11,file=gas_file)
        read(11,*)
        read(11,*) line%doublet_wavelength_1
        read(11,*) line%doublet_wavelength_2
        read(11,*) line%luminosity
        read(11,*) line%tot_flux
        if (lg_mcmc) then
           read(11,*)
        else
           read(11,*) line%doublet_ratio
        end if
        read(11,*)
        read(11,*) gas_geometry%clumped_mass_frac  !!!currently restricted to 0 or 1
        read(11,*) gas_geometry%ff
        read(11,*) gas_geometry%clump_power
        read(11,*)
        read(11,*) gas_geometry%v_max
        read(11,*) gas_geometry%r_max
        read(11,*) gas_geometry%r_ratio
        read(11,*) gas_geometry%v_power
        read(11,*) gas_geometry%rho_power
        read(11,*) gas_geometry%emis_power
        close(11)

        !read in dust options (for shell case)
        open(12,file=dust_file)
        read(12,*)
        if (.not. lg_mcmc) then
           read(12,*) dust%mass
        else
           read(12,*)
        end if
        if (dust_geometry%type == 'shell') then
            read(12,*)
            read(12,*) dust_geometry%clumped_mass_frac
            read(12,*) dust_geometry%ff
            read(12,*) dust_geometry%clump_power
            read(12,*)
            if (lg_mcmc) then
                read(12,*)
                read(12,*) dust_geometry%r_max
                read(12,*)
            else
                read(12,*) dust_geometry%v_max
                read(12,*) dust_geometry%r_max
                read(12,*) dust_geometry%r_ratio
            end if
            read(12,*) dust_geometry%v_power
            if (lg_mcmc) then
                read(12,*)
            else
                read(12,*) dust_geometry%rho_power
            end if
            read(12,*) dust_geometry%emis_power
            close(12)
        end if

        select case(dust_geometry%type)
            case ('shell')
                call check_dust_clumped()
        end select

        call check_scat_type()

        if ((gas_geometry%clumped_mass_frac /= 0) .and. (gas_geometry%clumped_mass_frac /= 1)) then
           print*,'ERROR:  Please enter a gas clump mass fraction equal to 0 or 1.  There is currently no provision for partial clumped emission. Aborted.'
           STOP
        end if

        !read in electron scattering options (if using electron scattering)
        if (lg_es) then
            !!temporarily prevent electron scattering - needs review.
            !print*, 'the electron scattering module needs review following updates to the code. please contact antonia.bevan.12@ucl.ac.uk.  aborted.'
            !stop
            open(13,file = e_scat_file)
            read(13,*)
            read(13,*) l_halpha
            read(13,*) es_temp
            close(13)
            if ((es_temp /= 5000) .and. (es_temp /= 10000) .and. (es_temp /= 20000)) then
                print*,'you have requested electron scattering.  please enter a gas temperature of 5000k, 10000k or 20000k'
                stop
            end if
        end if

    end subroutine read_input

end module input

