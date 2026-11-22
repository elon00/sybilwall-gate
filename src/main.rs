//! Offline peer-observation diagnostic. This is NOT Sybil resistance or security certification.
use std::env;
use std::process;

fn rejection_basis_points(accepted: u64, rejected: u64) -> Result<u64, &'static str> {
    let total = accepted.checked_add(rejected).ok_or("COUNT_OVERFLOW")?;
    if total == 0 {
        return Err("NO_OBSERVATIONS");
    }
    Ok(((rejected as u128 * 10_000) / total as u128) as u64)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 || args[1] != "inspect" {
        eprintln!("USAGE: sybilwall-gate inspect <accepted_u64> <rejected_u64>");
        process::exit(2);
    }
    let accepted = match args[2].parse::<u64>() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("INVALID_ACCEPTED_COUNT");
            process::exit(2);
        }
    };
    let rejected = match args[3].parse::<u64>() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("INVALID_REJECTED_COUNT");
            process::exit(2);
        }
    };
    match rejection_basis_points(accepted, rejected) {
        Ok(rate) => {
            let disposition = if rate >= 5_000 { "REVIEW" } else { "OBSERVE" };
            println!("OFFLINE_DIAGNOSTIC_ONLY rejection_bps={rate} disposition={disposition}");
        }
        Err(reason) => {
            eprintln!("{reason}");
            process::exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::rejection_basis_points;

    #[test]
    fn zero_rejections() {
        assert_eq!(rejection_basis_points(5, 0), Ok(0));
    }

    #[test]
    fn all_rejected() {
        assert_eq!(rejection_basis_points(0, 5), Ok(10_000));
    }

    #[test]
    fn fractional_rate_is_deterministic() {
        assert_eq!(rejection_basis_points(2, 1), Ok(3_333));
    }

    #[test]
    fn zero_observations_fail_closed() {
        assert_eq!(rejection_basis_points(0, 0), Err("NO_OBSERVATIONS"));
    }

    #[test]
    fn count_overflow_fails_closed() {
        assert_eq!(rejection_basis_points(1, u64::MAX), Err("COUNT_OVERFLOW"));
    }
}
